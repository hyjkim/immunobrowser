// from https://gist.github.com/mikehadlow/786386
// changed Suteki to EventBus because I have no idea what a suteki is
var EventBus = EventBus || {};
 
EventBus.newEventBus = (function(){
    var self = {};
    var subscriptions = {};
    var unsubscribeTokens = [];
    var subscriptionPointers = [];
 
    self.subscribe = function(nameOfMessage, callback){
        var i;
        var subscriptionPointer;
        var unsubscribeToken;
 
        if(typeof nameOfMessage !== 'string'){
            throw new Error("Suteki.eventBus.subscribe requires a first string argument 'nameOfMessage'");
        }
        if(typeof callback !== 'function'){
            throw new Error("Suteki.eventBus.subscribe requires a second function argument 'callback'")
        }
 
        if(!subscriptions[nameOfMessage]){
            subscriptions[nameOfMessage] = [];
        }
        subscriptions[nameOfMessage].push(callback);
 
        // package and return an unsubscribe token.
        subscriptionPointer = { nameOfMessage:nameOfMessage, callbackIndex: subscriptions[nameOfMessage].length-1 };
        i = subscriptionPointers.length;
        unsubscribeToken = {};
        subscriptionPointers[i] = subscriptionPointer;
        unsubscribeTokens[i] = unsubscribeToken;
        return unsubscribeToken;
    };
 
    self.publish = function(nameOfMessage, data){
        if(typeof nameOfMessage !== 'string'){
            throw new Error("Suteki.eventBus.publish requires a first string argument 'nameOfMessage'");
        }
        if(!data){
            throw new Error("Suteki.eventBus.publish on Message '"+nameOfMessage+"' requires a second argument 'data'");
        }
 
        var i;
        var callback;
 
        if(subscriptions[nameOfMessage]) {
            for(i=0; i<subscriptions[nameOfMessage].length; i++){
                callback = subscriptions[nameOfMessage][i];
                if(callback){
                    callback(data);
                }
            }
        }
    };
 
    self.unsubscribe = function(unsubscribeToken){
        var subscriptionPointer = subscriptionPointers[unsubscribeTokens.indexOf(unsubscribeToken)];
        subscriptions[subscriptionPointer.nameOfMessage][subscriptionPointer.callbackIndex] = null;
    };

    self.subscriptions = function () {
      return subscriptions;
    }
 
    return self;
});
