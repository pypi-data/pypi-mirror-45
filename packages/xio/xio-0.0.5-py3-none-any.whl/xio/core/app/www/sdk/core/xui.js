(function(){
    
    class AppTagHandler {

        constructor(name) {
            this.name = name
            this.handler = null
            this.events = {}
        }

        bind(handler) {
            this.handler = handler
            return this
        }

    }

    class AppTag extends AppTagHandler {

        constructor(name) {
            super(name)
            this.handlers = {}
        }
        type(name) {
            if (this.handlers[name]==null)
                this.handlers[name] = new AppTagHandler(name)
            return this.handlers[name]
        }
        bind(handler) {
            super.bind(handler)
            window.customElements.define(this.name, handler)
            return this
        }
        on(event,callback) {
            if (!this.events[event])
                this.events[event] = []
            this.events[event].push(callback)
        }
    }


    AppTags = function() {
        this._tags = {}    
        return this
    }
    AppTags.prototype.get = function (tagname) {
        var nodename = tagname.toUpperCase()
        if (this._tags[nodename]==null)
            this._tags[nodename] = new AppTag(tagname)
        var tag = this._tags[nodename]
        return tag
    }


    AppExts = function(app) {
        this._app = app    
        this._loading = {}
        this._basesrc = xio_sdk_baseurl+'/ext/'
        this._basesrc_component = xio_sdk_baseurl+'/components/'
        return this
    }
    AppExts.prototype._loadRequirements = function (basesrc, name, callback) {
        var self = this
        var data = self[name] || {}

        var requirements = data.requirements || []
        var nb_loaded = 0
        var nb_req = requirements.length

        var _load = function() {
            if (requirements.length) {
                var requirement = requirements.shift()
                var reqpath = basesrc+requirement
                self._app.load(reqpath,function() {
                    nb_loaded += 1
                    _load()
                })
            } else {
                self[name] =  self._loading[name]
                delete (self._loading[name])
                self._app.log.debug('loaded extension '+name)
                self._app.publish('app.ext.'+name)  
                if (callback) 
                    callback(self[name])
            }
        }
        _load()

    }
    AppExts.prototype.loadExt = function (name,callback) {
        var self = this
        if (!this[name] && !this._loading[name]) {

            xio.log.info('loading extension '+name)
            this._loading[name] = true

            var basesrc = this._basesrc+name+'/'
            $.getJSON( basesrc+'about.json', function( data ) {
                self[name] = data
                self._loadRequirements(basesrc,name,callback)
            }).fail( function(jqXHR, textStatus, errorThrown) { 
                self._app.log.error('loading extension '+name+' : '+textStatus) 
            })
        }
         
    }    
    AppExts.prototype.loadComponent = function (name,callback) {
        var self = this
        if (!this[name] && !this._loading[name]) {

            xio.log.info('loading component '+name)
            this._loading[name] = true

            var basesrc = this._basesrc_component+name+'/'
            var reqpath = basesrc+name+'.js'

            self._app.load(reqpath,function() {
                self._loadRequirements(basesrc,name,callback)
            })
        }
    } 

    class AppUi {

        constructor(app) {
            this.app = app
        }

        panel(id) {
            return $('#panel-'+id)[0]
        }
        confirm(config) {
            var d = $.Deferred(); 

            config.type = 'confirm'
            config.footer = `
                <button id="modalCancel" type="button" class="btn btn-secondary" data-dismiss="modal">Cancel</button>
                    <button id="modalConfirm" type="button" class="btn btn-primary">Confirm</button>
            `
            
            try {
                var popup = this.popup(config)
                popup.find('#modalCancel').unbind().click(function() {
                    d.reject(false);
                })
                popup.find('#modalConfirm').unbind().click(function() {
                    $('#appmodal').modal('hide');
                    d.resolve(true);
                })
                
                
            } catch(e) {
                alert('error '+e)
                d.resolve(false);
            }

            //d.resolve(true);
            return d.promise()
        }
        popup(config) {
            
            var popup = $(`<div  class="modal fade"  tabindex="-1" role="dialog">
              <div class="modal-dialog modal-dialog-centered" role="document">
                <div class="modal-content">
                  <div class="modal-header">
                    <h5 class="modal-title" >Confirm action</h5>
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                      <span aria-hidden="true">&times;</span>
                    </button>
                  </div>
                  <div class="modal-body">
                    
                  </div>
                  <div class="modal-footer">
                    
                  </div>
                </div>
              </div>

            </div>`)

            if (config.href)
                config.content = '<iframe src="'+config.href+'" style="width: 100%;height: 100%;position: relative;"></iframe>'

            if (config.title)
                popup.find('.modal-title').text(config.title)
            if (config.content)
                popup.find('.modal-body').html(config.content)

            if (config.footer)
                popup.find('.modal-footer').html(config.footer).show()
            else
                popup.find('.modal-footer').hide()
            popup.modal('show')
            return popup
        }

    }


	XioUi = function(endpoint,handler) {

        var self = this

        // global data
        this.data = {}
        this.data.i18n = {}

        this.dev = false
        this.debug = false

        // logs
        this.log = xio.log
        this.log.level = 'INFO'

        // user
        this.user = null 
        this.server = xio.app()
        this.handler = handler || '' 
        this.templates = { 
            load: function(path) {
                return $.get( self.nav.basepath+path)
            }
        }
        this._tags = new AppTags()
        this.tag = function(tagname) {
            return this._tags.get(tagname)
        }
        this.ui = new AppUi(this)
        this.cache = {}
        this._loaded = {}
        
        // ihm
        this._ready = false
        this.ext = new AppExts(this)
        //this.templates = new AppTemplates(this)
        //this.services = new AppServices(this)
        this.routes = new xio.routes()
        this.contracts = {} 
        this.topics = {
        }
        this.events = {
            'ready': []
        }
        this._enhances = []
        this.ihm = {
            'search': {
                'input': 'rr',
                'options': []     
            }      
        }    
        this.status =  {
            'message': 'App ready.'
        }

        // init nav

        var baseurl = document.location.origin
        var l = document.location.pathname.split('/');
        l.pop();
        var basepath = l.join('/')

        var hash = location.hash;
        if (hash) {
            var path = hash.slice(2)  
        } else {
            path = ''
        }
        this.device = {
            agent: navigator.userAgent,
            mobile: (/android|webos|iphone|ipad|ipod|blackberry|iemobile|opera mini/i.test(navigator.userAgent.toLowerCase())), 
            width: window.innerWidth,
            height: window.innerHeight
        }
        window.onresize = function() {  
            self.device.width = window.innerWidth
            self.device.height = window.innerHeight
        }
        this.layout = {
            slot: {}
        }
        this.nav = {
            basepath: basepath+'/',
            baseurl: baseurl+basepath,
            hashbang: '#!',
            location: location.hash,
            context: JSON.parse( sessionStorage.getItem('xio.nav.context') || '{}'),
            landing: '#home',
            language: 'fr',
            path: path,
            breadcrumb: [],
            request: {},
            sitemap: [],
            header: [],
            footer: [],
            //page: {},   // current page ctrl
            //context: {}, //
            current: {},
            getPath: function (path) {
                path = path || ''
                if (path.charAt(0)!='/')
                    return this.hashbang+this.path+'/'+path
                else
                    return this.hashbang+path
            },
            parse: function (location) {
                
                var context = {}
                // check session context in query
                if (location.href) {
                    console.log('location',location)
                    var query = location.search
                    if (query) {
                        var context = xio.tools.parseQuery(query)
                        console.log('found context',context)
                    }
                    var hash = location.hash
                } else {
                    var hash = location || ''
                }

                var info = hash.split('?')
                var hash = info[0];
                var query = info[1];
                var params = {}
                if (query) {
                    var params = xio.tools.parseQuery(query)
                }
                if (hash.startsWith(this.hashbang)) {
                    path = hash.slice(2)
                } else {
                    path = hash.slice(1)
                }
                return {
                    'path': path,
                    'query': params,
                    'context' : context
                }
            },
            setPath: function (path) {
                this.path = path
                this.breadcrumb = []
                var chref = this.hashbang
                var p = path.split('/')
                for (i in p) {
                    if (p[i]) {
                        chref = chref+'/'+p[i]
                        this.breadcrumb.push({
                            'name': p[i],
                            'href': chref
                        }) 
                    }
                }
                $('xio-breadcrumb').render(this.breadcrumb)
            },
            /*
            setContext: function (key,val) {
                if (val!=undefined) {
                    this.context[key]= val;
                } else {
                    this.context = key;
                }

            },
            */
            setContext: function(context) {
                sessionStorage.setItem('xio.nav.context',JSON.stringify(context))
            },
            updateContext: function (context) {
                for(key in context) {
                    this.context[key] = context[key];
                }
            },
            goto: function (path) {
                var newpath = this.getPath(path)   
                location.hash = newpath
            },
        }

        // fix initial context
        var parsed = this.nav.parse(window.location)
        if (parsed.context && !$.isEmptyObject(parsed.context)) {
            console.log('save context', parsed.context)
            this.nav.setContext(parsed.context)
            // reload
            var loc = window.location
            window.location.replace(loc.protocol+'//'+loc.hostname+loc.pathname+'#'+loc.hash)

        }
       


		return this
	}
    XioUi.prototype.init = function () {

        var self = this
        this.log.info('init app')

        // capture body
        this.root = $('xio-app, xio-page, xio-section').first()
        if (this.root)
            this.root.css('visibility', 'hidden');
        //$('body').html('<div style="display: table; width:100%; height:100%"><div style="display: table-cell; vertical-align: middle; "><div style="width:40%; margin-left: auto; margin-right: auto;text-align: center">loading ...</div></div></div>')


        // globals templates
        /*
        var d1 = self.load( this.nav.basepath+'sdk/core/templates.html', function(  ) {
            self.log.info('templates loaded')
        })
        */

        // about app

        var global_requirements = [
            'sdk/components/input',
            'sdk/components/resource',
            'sdk/components/onboarding',
            'ethereum',
            'bootstrap',
        ]


        var d2 = $.getJSON( this.nav.basepath+'about.json').then( function( data ) {
            
            var d = $.Deferred(); 
            self.about = data || {'requirements':[]}

            if (self.about.sitemap) {
                self.nav.sitemap = self.about.sitemap //.concat(self.about.sitemap) // pb doublon concat 
            }

            // global reqs

            $.each(global_requirements, function( i,src ) { 
                self.about.requirements.push(src)
            }) 
            
            // load requirements
            var nb_requirements = self.about.requirements.length
            var nb_requirements_loaded = 0
            if (!nb_requirements) { 
                self.publish('ready')
                return    
            }
            $.each(self.about.requirements, function( i,name ) { 
                // TOFIX self.ext.load 
                // name is confuse : requirement could be file
                self.load(name, function() {
                    nb_requirements_loaded += 1
                    if (nb_requirements_loaded>=nb_requirements) {
                        d.resolve(true)
                    }     
                })
            }) 

            // init nav & layout data
            $.each(self.nav.sitemap, function( i,page ) { 
                //page.id = page.path //.slice(1)
                if (!page.id) {
                    page.id = self.uuid()
                }
                self.routes.bind(page.path,page)

                var slot = page.slot || 'header'
                var slots = slot.split(' ')
                for (var i in slot) {
                    slot = slots[i]
                    if (!self.layout.slot[slot]) {
                        self.layout.slot[slot] = {}
                    } 
                    if (!self.layout.slot[slot]['links']) {
                        self.layout.slot[slot]['links'] = []
                    } 
                    self.layout.slot[slot]['links'].push(page) 
                }
           
            })    
            
            return d.promise()

        })

        return $.when( d2).then(function (r2) {
            // init user

            XioUser.loadSession()

            self.user = xio.context.user
            var endpoint = xio.context.endpoint || document.location.origin

            // init server
            if (xio.context.server) {
                self.server = xio.context.server // overwrite default server
            } else if (self.user && endpoint) {
                return self.user.connect(endpoint).then(function(server) {
                    xio.context.server = server
                    self.server = server
                })
            } 

        }).then(function (r2) {
            self.log.info('APP READY.')
            self._ready = true
            self.emit('ready')
            self.run()
        })



    }
    XioUi.prototype.run = function (path) {

        console.log('RUN',this.root, path)

        var self = this

        path = path || null
        
        this.log.info('RUN '+path)
        this.log.info('APP RUN. ',this.root)

        // prop
        this.prop('dev', this.dev)
        this.prop('debug', this.debug)
        this.prop('mobile', this.device.mobile)
        this.prop('user', (this.user && this.user.id) )

        // render
        
        var data = {
            'app': this,
            '_': this.data.i18n[this.nav.language]
        }

        return this.root.render(data).then(function() {
            self.root.css('visibility', 'visible');
            self.root.show()
            console.log('RUN SHOW ',path)
            if (!path) {
                if (window.location.hash) {
                    path = window.location.hash
                } else {
                    path = app.nav.landing || this.root.children('xio-page').first().attr('id')
                } 
            } else {
                window.location.href = path
            }
            self.emit('run')
            self.render(path)
        })
    }
    XioUi.prototype.redirect = function (href) {
        app.run(href)
    }
    XioUi.prototype.uuid = function () {
        var dt = new Date().getTime();
        var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            var r = (dt + Math.random()*16)%16 | 0;
            dt = Math.floor(dt/16);
            return (c=='x' ? r :(r&0x3|0x8)).toString(16);
        });
        return uuid;
    }
    XioUi.prototype.bind = function (path,handler) {
        this.routes.bind(path,handler)
    }
    XioUi.prototype.schedule = function (id,t,handler) {
        xio.schedule(id,t,handler)
    }
    XioUi.prototype.enhance = function (el) {
        if (typeof el === "function") {
            // add enhancement handler
            this._enhances.push(el)
        } else {
            // enhance element
            $(this._enhances).each(function(){
                try {
                    //console.log('enhance',el,this)
                    this.apply(el)
                } catch(error) {
                    this.log.error(error);
                }
            })
        }

        var self = this
        /*
        // handle relative link
        $(el).find("a[href^='#./']").click(function(e) {
            e.preventDefault()
            try {
                //$(this).addClass('active')

                var element = $(el).closest('xio-resource')[0]
                //var req = xio.request('GET',$(this).attr('href').slice(3))
                var method = $(this).attr('href').slice(4).toUpperCase()
                var req = xio.request(method)
                element.render( req )
            } catch(error) {
                console.log(error);
            }
            return false;
        })
        */

    }
    XioUi.prototype.prop = function (key,value) {
        if (value==undefined)
            return $('body').hasClass('xio-'+key)
        if (value)
            $('body').addClass('xio-'+key)
        else
            $('body').removeClass('xio-'+key)
    }
    XioUi.prototype.login = function (seed,password,endpoint) {
        // init user
        console.log('LOGIN', seed,password,endpoint)
        var self = this
        return XioUser.login(null,seed).then(function(user) {
            self.user = user
            return self.user.connect( endpoint ).then(function(server) {
                self.server = server
                self.emit('login', self.user)
                self.run()
            })
        })
    }

    XioUi.prototype.logout = function (callback) {
        this.emit('logout', this.user)
        this.user.logout()
        this.prop('user', false )
        this.run('#')
    }

    XioUi.prototype.load = function (src,callback) {
        var self = this

        // handle xio server resource

        var filename = src.split('/').pop()
        var info = filename.split('.')
        if (info.length==1) {
            if (src.charAt(0)=='/') {
                var type='unknow'
            }
            else if (src.startsWith('sdk/components')) {
                var type='component'
                var src = src.split('/').pop()
            } else {
                var type='ext'
                var src = src.split('/').pop()
            }
        } else {
            var type = info.pop()
        }



        this.log.info('loading ... '+src)


        // fix new version
        if (type=='html') {
            if (!this._loaded[src]) {
                return this._loaded[src] = $.get( src ).then( function(content) {
                    if (callback)
                        callback(content)
                    return content
                })
            }
            return this._loaded[src]
        }

        if (!this._loaded[src]) {
            this._loaded[src] = {
                'status': 0,
                'callbacks': []
            }
            if (type=='ext') {
                var self = this
                // fix bad src which contain basepath of caller ext
                var src = src.split('/').pop()
                self.ext.loadExt(src, function() {
                    self.log.info('LOADED '+src)
                    callback()
                })
            }
            else if (type=='component') {
                var self = this
                // fix bad src which contain basepath of caller ext
                var src = src.split('/').pop()
                self.ext.loadComponent(src, function() {
                    self.log.info('LOADED '+src)
                    callback()
                })
            }
            else if (type=='js') {
                var head = document.getElementsByTagName('head')[0];
                var script = document.createElement('script');
                script.type = 'text/javascript';
                var self = this
                script.onload = function() {
                    self.log.debug('LOADED '+src)
                    self._loaded[src].status = 200    
                    for (var i in self._loaded[src].callbacks) {
                        var h = self._loaded[src].callbacks[i]
                        h()
                    }
                }
                script.src = src;
                head.appendChild(script);

            }

            else if (type=='css') {
                var head = document.getElementsByTagName('head')[0];
                var link = document.createElement('link');
                link.type   = 'text/css';
                link.rel    = 'stylesheet';
                //link.onload = () => { resolve(); app.log.info('style has loaded'); };
                link.href   = src;
                head.appendChild(link);
                this._loaded[src].status = 200 
                for (var i in this._loaded[src].callbacks) {
                    var h = this._loaded[src].callbacks[i]
                    h()
                }
            }
            else if (type=='json') {
                return $.getJSON( src ).then( function(content) {
                    self._loaded[src].status = 200
                    self._loaded[src].content = content
                    if (callback)
                        callback(content)
                    return content
                })
            }
            else if (type=='html') {
                //alert(src)
                return $.get( src ).then( function(content) {
                    //alert('loaded '+content)
                    self._loaded[src].status = 200
                    self._loaded[src].content = content
                    if (callback)
                        callback(content)
                    return content
                })
            } 
            else if (type=='unknow') {
                return $.get( src ).then( function(content) {
                    self._loaded[src].status = 200
                    self._loaded[src].content = content
                    if (callback)
                        callback(content)
                    return content
                })
            }
            /*
            // html import disabled from polyfil
            else if (type=='html') {
                var link = document.createElement('link');
                link.rel = 'import';
                link.href = src;
                var self = this
                link.onload = function(e) { 
                    self.log.info('LOADED '+src)
                    $(this.import).find('template[id]').each( function() {
                        var id = $(this).attr('id');
                        self.templates[id] = this
                    })
                    self._loaded[src].status = 200    
                    for (var i in self._loaded[src].callbacks) {
                        var h = self._loaded[src].callbacks[i]
                        h()
                    }
                };
                link.onerror = function(e) {
                    self.log.error('unable to load '+src)
                };
                document.head.appendChild(link);
            }
            */
        }
        if (this._loaded[src].status==200) {
            if (callback) {
                callback(self._loaded[src].content)
            }
            else {
                var d =  $.Deferred(); 
                d.resolve(self._loaded[src].content)
                return d.promise()
            }
        } else if (callback) {
            this._loaded[src].callbacks.push(callback)
        }
        else {
            var d =  $.Deferred(); 
            this._loaded[src].callbacks.push( function(content) {
                d.resolve(content)
            })
            return d.promise()
        }
    }

    XioUi.prototype.scroll = function (target) {
        $('body,html').animate(
            {'scrollTop':target.offset().top - 90},
            900
        );
    }

    XioUi.prototype.template = function (template,data) {
        return this.templates[template]
    }


    XioUi.prototype.ready = function (callback) {
        if (this._ready) {
            callback()
        } else {
            this.events['ready'].push(callback)
        }
    }

    XioUi.prototype.publish = function (topic,data) {
        this.log.debug('publish '+topic,data)  
        for (i in this.topics[topic]) {
            try {
                var callback = this.topics[topic][i]
                callback(data) 
            } catch(error) {
                this.log.error(error);
            }
        }
    }
    XioUi.prototype.subscribe = function (topic,callback) {
        this.log.debug('subscribe '+topic,callback)
        if (!this.topics[topic])
            this.topics[topic] = []     
        this.topics[topic].push(callback)
    }
    XioUi.prototype.on = function(event,callback) {
        if (!this.events[event]) {
            this.events[event] = []
        }
        this.events[event].push(callback)
    }

    XioUi.prototype.emit = function(event,data) {
        if (this.events[event]) {
            $(this.events[event]).each(function(){
                try {
                    console.log('emit',event,data)
                    this(data)
                } catch(error) {
                    console.log(error);
                }
            })
        }
    }

    XioUi.prototype.renderFallback = function (path,data) {
        // born to be overwrited
        // if hash try #home to /home
        if (path.startsWith('#'))
            return this.render('/'+path.slice(1))
        
    }
    
    XioUi.prototype.render = function (path,data) {
        console.log('====== APP RENDER 1 '+path,data) 
        var self = this
        //this.log.info('====== APP RENDER '+path,data) 
        if (path.startsWith('#.')) {
            path = app.nav.getPath( path.slice(3) )   
            location.replace(path);
            return
        } if (path.startsWith(this.nav.hashbang)) {
            var parsed = app.nav.parse(path)
            path = parsed.path
            data = parsed.query 
        } else if (path.startsWith('#')) {
            var parsed = app.nav.parse(path)
            path = parsed.path
            data = parsed.query 
        } 
        console.log('====== APP RENDER 2 '+path,data) 

        this.nav.setPath(path)

        // handle language

        if (!path && data && data.lang) {
            app.nav.language = data.lang
            app.run('#')
            return true;
        }


        // step1 : find route handler + element
        var p = path.split('/')


        var route = this.routes.getClosestHandler(path)
        //var route = this.routes.getHandler(path)
        /*
        // if no route find best handler
        if (!route) {
            var ptest = path.split('/').slice(0,-1).join('/')
            var route = this.routes.getHandler(ptest)
        }
        */
        console.log('get route',path,route)

        if (route) {
            // render by callable function
            console.log(route)
            var handler = route.handler
            var postpath = route.postpath

            var context = route.context
            // check if page context defined
            if (handler.context) {
                for (var key in handler.context) {
                    context[key] = handler.context[key]
                }
            }

            // check if handler is a nav page
            if (handler && handler.path) {
                var el = $('xio-page[path="'+handler.path+'"]')
                handler = el[0]
            }
        } else {
            // render by element
            var el = $('#'+p[0])
            var handler = el[0]
            var postpath = p.slice(1).join('/')
            var context = {}
        }

        if (!handler) {
            console.log('... no handler') 
            // fallback ??
            return
        }

        // step2 : build req
        
        var req = xio.request('GET',postpath,data,{},context)
        req.fullpath = req.path

        // step2 : setup nav current info
        app.nav.current.path = path
        app.nav.current.page = el
        app.nav.current.context = context 
        app.nav.current.postpath = postpath 
        app.nav.current.request = req 

        // handle

        console.log('====== #',handler,'RENDER ',req) 
        if (handler.render) {
            // force reload (eg same page with different context)
            handler.nx.rendered = false
            var result = handler.render(req)
        } else {
            var result = handler(req)
        }
        return $.when(result).then(function() {
            self.emit('render',req)
        })
    }


})();



window.app = new XioUi()

$(document).ready( function() {
    app.init()
})

$(window).bind( 'hashchange', function(e) { 
    //console.log('hashchange ...', location.hash)
    var hash = location.hash
    app.render(hash)
});



// overide/extend jquery

var oHtml = jQuery.fn.html;
jQuery.fn.html = function() {
    var result = oHtml.apply(this, arguments);
    app.enhance(result)
    return result
};

$.fn.extend({


    render: function (data,template,debug) {

        var el = this[0]

        // cas des xio-elements 
        if (el && el.render) {
            return el.render(data)
        }

        /*
        else {
            // to remove ???
            // custom tag -> call element render for rebuild it
            //if (el.render)
            //    return el.render() 
        }
        */

        //app.log.info('.................... applyTemplate')
        var id = this.attr('id')
        // auto register template
        if (!template && id && !app.templates[id]) {
            
            if (id) {
                // lookup template
                var tpl = this.children('template').first()
                if (tpl) {
                    app.templates[id] = tpl
                    this.html()
                }
            }
        }


        function applyTemplate(tpl,data) {

            // prevent sub template rendering (( not usable because of js code
            var subtpl = false
            var $tpl = $("<root/>")
            $tpl.html(tpl)
            $tpl.find('template').each(function() {
                this.innerHTML = this.innerHTML.replace(/{{/g, "@((").replace(/}}/g, "))@") 
                subtpl = true
            })

            var html = Mustache.to_html( $tpl.html() ,data);
            if (subtpl) {
                html = html.replace(/@\(\(/g, "{{").replace(/\)\)@/g, "}}")
            }
            
            return html
        }
        

        function _render(el,data,template,debug) {

            if (!el.xiotemplate) {
                if (template) 
                    el.xiotemplate = template 
                else
                    el.xiotemplate = $(el).html()   
            }

            var html = applyTemplate(el.xiotemplate,data) //Mustache.to_html(el.xiotemplate,data);
            $(el).html(html)
        }

        //console.log('render',this,data,el)

        if (!el) {
            //app.log.info('template not found :',this)
            return 
        }

        /*
        // to remove 
        else if (id && app.templates[id]) {
             console.log('id',id,app.templates[id])
            var tpl = app.templates[id].html()
            var html = applyTemplate(tpl,data)
            this.html(html)
            return this
        }
        */

        if (el._template) {

            //var html = Mustache.to_html(el._template,data);
            var html = applyTemplate(el._template,data)
            this.html(html)
            return
        }
        if (this.prop("tagName").toLowerCase()=='script') {
            // script -> return html
            //var html = Mustache.to_html(this.text(),data);
            //return html
            return applyTemplate(this.text(),data)
        }
        else if (this.prop("tagName").toLowerCase()=='template') {
            // template -> return html
            //var html = Mustache.to_html(this.html(),data);
            return applyTemplate(this.html(),data)
        } 
        
        return this.each(function() {
            _render(this,data,template,debug)
            return this
        });
    },


    enhance: function () {
        /*
        post rendering globals actions
        */
        app.enhance(this)
        return this
    },

});


/////// tools

function json2html(data) {
    var html = '';

    if (Array.isArray(data)) {
        html += '<table class="table  table-sm">';
        for (i in data) {
            var value = data[i];
            if (value) {
                html += '<tr>';
                html += '<td>'+json2html(data[i])+'</td>';
                html += '</tr>';
            }
        }
        html += '</table>';
    } else if (typeof data==="object" ) {
        html += '<table class="table  table-sm">';
        for (i in data) {
            var value = data[i];
            if (value) {
                html += '<tr>';
                html += '<th valign="top">'+i+'</th>';
                html += '<td>'+json2html(data[i])+'</td>';
                html += '</tr>';
            }
        }
        html += '</table>';
    } else {
        html = data;
    }
    return html;
}




