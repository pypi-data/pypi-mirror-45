(function(){

    TEST_SEED       = 'very weak seed' 
    TEST_SHA256     = 'c55487a5417d759e04f5d57d34e11151e2fc04a2048c8b19dca9ed3c59a8a49e'
    TEST_PRIVATE    = '37b75e9adbf125f93fb14b41cb4fe530e6dd6e4a9c854ab1b33c513cc561e05b'
    TEST_PUBLIC     = '145a1afd1792a23c79eb267ec53ae02117d44a13659cb44f7ec4de3579bbf8a7'


    function bytesToHex(s) {
        var web3 = new Web3();
        return web3.utils.bytesToHex(s).slice(2)
    }

    function hexToBytes(h) {
        var web3 = new Web3();
        return web3.utils.hexToBytes('0x'+h)
    }

    function sha3(txt) {
        var web3 = new Web3();
        return web3.utils.sha3(txt)
    }


    XioNaclAccount = function(private,seed,token) {
        var private = private || null
        this.private = null
        this.public = null

        if (private) {
            private = hexToBytes(private)
            this._keyPair = nacl.sign.keyPair.fromSecretKey( Uint8Array.from( private )  ); // nacl.util.decodeUTF8(private)
        } else if (seed) {

            seed = sha256(seed)
            seed = hexToBytes(seed)
            seed = Uint8Array.from( seed )
            this._keyPair = nacl.sign.keyPair.fromSeed( seed )

        } else {
            this._keyPair = nacl.sign.keyPair();
        }

        this.private = bytesToHex( this._keyPair.secretKey ) /////// tofix priv+pub (64) au lieu de priv(32)
        this.public = bytesToHex( this._keyPair.publicKey )

        this.sign = function(message) {
            return this._account.sign(message)
        }
        
        this.generateToken = function() {
            var timestamp = Math.round((new Date()).getTime() / 1000) + 60*5;
            var id = this.public
            var nonce = timestamp.toString()
            var sign = this.sign(nonce)
            var token = id+'-'+nonce+'-'+sign.v+'-'+sign.r+'-'+sign.s
            return token
        }
        return this
    }
    
    XioEthereumAccount = function(private,seed,token) {
        var private = private || null

        this.web3 = new Web3();
        this.private = null
        this.public = null
        this.address = null

        if (seed) {
            //var newaccount = self.web3.eth.accounts.create()
            var key = this.web3.utils.sha3(seed)
            this._account = this.web3.eth.accounts.privateKeyToAccount(key) //////// ?????? devriat etre from seed ??

        } else if (private) {

        } else {
            this._account = this.web3.eth.accounts.create()
        }

        this.private = this._account.privateKey
        this.address = this._account.address

        this.sign = function(message) {
            return this._account.sign(message).signature
        }
        
        this.generateToken = function() {
            var timestamp = Math.round((new Date()).getTime() / 1000) + 60*5;
            var id = this.address
            var nonce = timestamp.toString()
            var sign = this.sign(nonce)
            var token = id+'-'+nonce+'-'+sign.v+'-'+sign.r+'-'+sign.s
            return token
        }
        return this
    }

    XioAccount = function(private,seed,token) {
        this._handler = new XioNaclAccount(private,seed)
        this.private = this._handler.private
        this.public = this._handler.public
        this.address = this._handler.address || this._handler.public
        this.account = function(realm) {
            var seed = this.private.slice(0,64) // fix car les 64 autres bytes sont la publicc key
            return new XioEthereumAccount (null,seed)
        }
        this.generateToken = function() {

        }
        return this
    }


    XioUser = function(private,seed) {
        this.account = new XioAccount(private,seed)
        this.id = this.account.address
        this.token = this.account.generateToken()
        return this
    }


    /* static */
    XioUser.loadSession = function() {
        session = JSON.parse( localStorage.getItem('xio.user.session') || '{}')
        if (session.private) {
            var user = new XioUser(session.private)
            user.id = session.id
            user.token = session.token
            user.scheme = session.scheme

            var xioauth = encodeURIComponent(user.token)
            document.cookie = "XIO-AUTH="+xioauth+";path=/";

            xio.context.user = user
            xio.context.endpoint = session.endpoint
        }
        return {}
    }


    XioUser.login = function(private,seed,password) {
        /* generate xio keystore */
        var user = new XioUser(null,seed)
        user.saveSession()
        return Promise.resolve(user)
    }

    /* instances */


    XioUser.prototype.connect = function(endpoint) {
        /* generate token and identity for this endpoint */
        var self = this
        xio.log.info('connect '+endpoint) 

        this.token = this.generateToken()

        this.endpoint = endpoint /// to fix, remove this.endpoint
        self.saveSession()

        var server = xio.client(endpoint)
        server._token = this.token
        return server.connect().then(function() {
            xio.log.info('connected')
            return server
        })
        //return Promise.resolve(server)
    }

    XioUser.prototype.generateToken = function(scheme) {
        scheme = 'xio/ethereum' 
        var ethaccount = this.account.account('ethereum')
        this.id = ethaccount.address
        var iss = ethaccount.address
        var iat = Math.round((new Date()).getTime() / 1000);
        var exp = iat+3600;
        //"jti": to_string(uuid.uuid4()),
        // need to sort key for sig check
        
        var header = {
            "typ": "JWT",
            "alg": scheme
        }
        var body = {
            "iat": iat,
            "iss": iss,
            "exp": exp,
            "sub": iss
        }
        sig = ethaccount.sign( JSON.stringify(body) ) 
        console.log(header,body,sig)
        var token = btoa( JSON.stringify(header)) +'.'+btoa( JSON.stringify(body) )+'.'+btoa( sig )
        return token
    }


    XioUser.prototype.saveSession = function() {
        localStorage.setItem('xio.user.session',JSON.stringify({
            'id': this.id,
            'private': this.account.private,
            'scheme': this.scheme,
            'token': this.token,
            'endpoint': this.endpoint
        }))
    }
    XioUser.prototype.logout = function() {
        this.id = null
        this.name = null
        this.token = null
        this.address = null
        this.account = null
        localStorage.removeItem('xio.user.session')
        document.cookie.split(";").forEach(function(c) { document.cookie = c.replace(/^ +/, "").replace(/=.*/, "=;expires=" + new Date().toUTCString() + ";path=/"); });
    }




})();



