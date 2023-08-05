


class XIOElement extends HTMLElement {
    
    constructor() {
        super();   

        //alert( this.getAttribute('type') )

        var self = this
        this.nx = {}    
        this.nx.children = []
        this.nx.events = {}
        this.nx.getParent = function() {
            console.log($(self).closest('body').html())
            return $(self).parent().closest('.xio-element')[0]
        }
        
    }

    connectedCallback() {
        var self = this

        // bug with app : not initaalized !
        if (app._ready) {
            this.log('connectedCallback')
            //window.setTimeout(function() {
                self._init().then(function() {
                    // auto render for no-hidden element (eg page)

                    if ( self.nx.hidden )
                        $(self).hide()
                    else
                        return self.render()
                        
                })
            //},0)
        }

    }

    _getHandler() {

        if (this.nx.handler)
            return this.nx.handler

        var type = $(this).attr('type')
        if (type) {
            var handlercls = app.tag(this.nodeName).type(type).handler
            if (handlercls) {
                this.nx.handler = new handlercls()
                this.nx.handler.init(this)
                
            }
        }
        return this.nx.handler
    }

    init() {
        // to be overwrited
    }

    _init() {
        var self = this
        this.nx.parent = $(this).parent().closest('.xio-element')[0]
        this.nx.debug = $(this).hasClass('debug')
        if (this.nx.parent)
            this.nx.parent.nx.children.push(this)

        // handle handler by type
        this.nx.handler = this._getHandler()

        if (this.nx.initialized) {
            return $.when( false )
        }
        this.log('init')

        this.nx.initialized = true

        if (!this.id) {
            this.id = app.uuid()
        }

        $(this).addClass('xio-element')
        var d = this.init()
        return $.when( d ).then(function() {
            if (self.nx.handler && self.nx.handler.init)
                return self.nx.handler.init(self)
        })
    }


    _load() {
        var self = this

        if (this.nx.loaded)
            return this.nx.loaded
        
        this.log('LOAD')
        
        var d1 = self._getData()
        var d2 = self._getTemplate()
        var d3 = self._getContent()

        this.nx.loaded = $.when(d1,d2,d3).done(function(data,template,content) {
            self.nx.data = data
            self.nx.template = template
            self.nx.content = content
            self.log('LOADED',self.nx)
        })
        return this.nx.loaded
    }


    _getContent() {
        var self = this
        var result = null
        var src = $(this).attr('src')
        if (src) {
            
            return app.load(src).then(function(content) { 

                // handle json (cf cio-include)
                if (content instanceof Object)
                    content = $.trim( JSON.stringify(content) )

                return content
            })
        } else if (self.getContent) {
            return self.getContent()
        } else {
            return self.innerHTML
        }
    }

    _getTemplate() {
        var self = this
        
        if (this.nx.handler && this.nx.handler.getTemplate)
            return this.nx.handler.getTemplate() 

        // test default/rendering template
        var cfg = app.tag(this.nodeName)
        if (cfg.template)
            return cfg.template

        var src = $(this).attr('template')
        if (src) {
            return app.load(src).then(function(template) { 
                return template
            })
        } else if (self.getTemplate) {
            return self.getTemplate()
        }
    }

    _getData() {
        if (this.nx.data)
            return this.nx.data
        var self = this
        var src = $(this).attr('data')
        if (src) {
            return app.load(src).then(function(data) { 
                return data
            })
        } else if (self.getData) {
            return self.getData()
        }
    }


    render(req) {
        var self = this

        // force element init (eg xio-app)
        return this._init().then( function() {

            return self._load().then( function() {

                if (self.nx.rendered)
                    return 

                self.log('RENDER')
                console.log('RENDER ????')
                
                var content = self.nx.content
                var template = self.nx.template
                var data = self.nx.data || {}
                data['app'] = app

                if (template) {
                    var $template = $('<div>'+template+'</div>') // pb avec find .slot si tag template
                    $template.find('.slot').html(content)
                } else {
                    var $template = $('<template>'+content+'</template>')
                }
                var html = $template.render(data)
                self.nx.rendered = html
                $(self).html(html)
                

            }).then(function(){
                if (self.nx.handler && self.nx.handler.render)
                    return self.nx.handler.render(req)
            }).then(function(){
                self.emit('rendered')
            })

        })
    }



    log(msg) {
        var args = $.makeArray(arguments)
        args.unshift('===================================== #'+this.nodeName)
        if (this.nx.debug)
            console.log.apply(this,args)
    }


    on(topic,callback) {
        if (!this.nx.events[topic])
            this.nx.events[topic] = []
        this.nx.events[topic].push(callback)
    }

    emit(event,data) {
        var self = this
        self.log('emit',event)
        if (this.nx.events[event])
            $(this.nx.events[event]).each(function(){
                this.apply(self, [data])
            })
        if (app.tag(this.nodeName).events[event])
            $(app.tag(this.nodeName).events[event]).each(function(){
                this.apply(self, [data])
            })
        // handle jquery event ---- bug infinit loop
        //alert('?')
        //$(this).trigger( event, [data]);
    }

    _refresh() {

        //alert( this.nodeName+' refresh')
        var counter = 0
        for (var i in this.nx.children) {
            var child = this.nx.children[i]
            if (child.nx.status!=9) {
                return 
            }
        }
        //alert(this.nodeName+' ready '+i)
        this.render()
    }




    
}


app.tag('xio-app').bind( class extends XIOElement {

    getTemplate() {
        return `<header id="xio-app-header">
            <nav id="xio-app-nav" class="navbar navbar-toggleable-md fixed-top">
                <div class="container ">
                    <a class="navbar-brand" href="#">
                        <img src="sdk/images/icon.png" height="36" class="d-inline-block align-top" alt="" > {{app.about.name}} 
                    </a>

                    <ul class="nav nav-pills mr-auto ">
                      {{#app.layout.slot.header.links}}
                        <li class="nav-item"><a class="nav-link" href="{{path}}" >{{label}}</a> </li> 
                      {{/app.layout.slot.header.links}}
                    </ul>
                          
                    <ul class="nav float-xs-right">

                        {{#app.user.id}}
                        
                            {{#app.about.search}}
                                <xio-search></xio-search>
                            {{/app.about.search}}
                        
                          <li class="nav-item dropdown">
                            <a class="nav-link dropdown-toggle" data-toggle="dropdown" data-nx-binded="app.user.id">{{app.user.id}}</a>
                            <div class="dropdown-menu" >
                              {{#app.layout.slot.user.links}}
                                <a class="dropdown-item" href="{{path}}">{{label}}</a>
                              {{/app.layout.slot.user.links}}
                              <div class="dropdown-divider"></div>
                              <a class="dropdown-item" href="javascript:app.logout()">LOGOUT</a>
                            </div>
                          </li>
                        {{/app.user.id}}
                        {{^app.user.id}}
                          {{#app.about.user.link}}
                          <li class="nav-item"><a class="nav-link btn btn-primary btn-sm" href="{{app.about.user.link}}" >CONNECT</a> </li> 
                          {{/app.about.user.link}}
                        {{/app.user.id}}
                    </ul>
                </div>

            </nav>

            {{#app.user.id}}
            <nav id="xio-app-toolbar" class="navbar navbar-toggleable-md fixed-top" >
                <div class="container ">
                    
                    <ul class="nav nav-pills mr-auto ">
                      {{#app.layout.slot.toolbar.links}}
                        <li class="nav-item"><a class="nav-link" href="{{path}}" >{{label}}</a> </li> 
                      {{/app.layout.slot.toolbar.links}}
                    </ul>
                          
                    <ul class="nav float-xs-right">
                      {{#app.layout.slot.toolbar.button}}
                        <li class="nav-item"><a class="nav-link" href="{{path}}" >{{label}}</a> </li> 
                      {{/app.layout.slot.toolbar.button}}
                    </ul>
                    <xio-search class="xio-dev"></xio-search>
                </div>
            </nav>

            {{/app.user.id}}

        </header>



        <div style="padding-top: 100px; padding-bottom: 100px;" class="container">  

            <div class="container ">
                <xio-breadcrumb>aa</xio-breadcrumb>
            </div>

            <xio-page id="login">
                landing
                <xio-onboarding>
                </xio-onboarding>
            </xio-page>

            <div class="slot">
            </div>



        </div>


        <footer id="xio-app-footer">
            <nav  class="navbar navbar-toggleable-md  fixed-bottom">


                <div class="container">

                    <div style="display: inline-block;vertical-align: middle; text-align: center; display: none" data-xio-if="app.status.loading">
                      <i class="fa fa-refresh fa-spin"  style="vertical-align: middle; opacity: 0.5">
                      </i> LOADING ...
                    </div> 

                    <span class="navbar-text mr-auto text-muted">
                     {{{app.about.footer.text}}} 
                    </span>



                    </ul>
                    <ul class="nav nav-pills float-xs-right">
                        {{#app.layout.slot.footer.links}}
                          <li class="nav-item"><a class="nav-link" href="{{path}}">{{label}}</a> </li> 
                        {{/app.layout.slot.footer.links}}
                        
                    </ul>
                </div>
            
            </nav>
        </footer>
        `;
    }
    

    init() {
        $(this).hide()
    }
    render() {
        var self = this
        return super.render().then( function() {
            $(self).show()
        })
    }
    
})



app.tag('xio-page').bind( class extends XIOElement {

    getTemplate() {
        return `<div class="page slot">
                       page
                    </div>
        `
    } 
    
    init() {
        this.nx.hidden = true
    }

    show() {
        $('xio-page')[0].hide()
        $(this).show()
    }
    hide() {
        $(this).hide()
    }
    render() {

        var self = this
        return super.render().then( function() {
            self.show()
        })
    }
    
})

window.customElements.define('xio-section', class extends XIOElement {

    getTemplate() {
        return `<section class="slot"></section>`
    } 
    


})


window.customElements.define('xio-data', class extends XIOElement {

    render() {
        var self = this
        return super.render().then( function() {
            self.raw = $.trim( self.nx.content )
            self.name = $(self).attr('name')
            try {
                self.data = JSON.parse( self.raw )
                if (self.nx.parent) {
                    if (self.nx.parent.nx.data==undefined)
                        self.nx.parent.nx.data = {}
                    self.nx.parent.nx.data[self.name] = self.data
                }
            } catch(e) {
                $(self).attr('error',e)
            }
        })
    }
    
})



window.customElements.define('xio-include', class extends XIOElement {

    render() {
        var self = this
        this.src = $(this).attr('src')
        if (this.src) {
            return app.load(this.src).then( function(content) {
                if (content instanceof Object)
                    content = $.trim( JSON.stringify(content) )
                $(self).replaceWith(content)
            })
        }

    }
    
})

/*

window.customElements.define('xio-script', class extends XIOElement {

    render() {
        var code = $(this).text()
        var h = Function(code);
        //$(this.html() = 
        var element = this.nx.parent
        h.call(element)   
    }
}) 


*/

window.customElements.define('xio-script', class extends XIOElement {

    render() {
        var self = this
        $(this).hide()
        this.event = $(this).attr('on')
        this.code = $.trim( this.innerHTML )
        this.handler = Function(this.code);
        
        if (event) {
            this.nx.parent.on(this.event, function(data) {
                self.handler.apply(this,data)   
            })
        } else {
            self.handler.apply(this.nx.parent) 
        }

    }
    
})
