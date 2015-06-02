    <script language="javascript" type="text/javascript">
        function init() { 
            output = document.getElementById("output");
            testWebSocket();
         }
        var wsUri = 'ws://192.168.113.195:8080/websocket';
        function onMessage(evt){
            var oldHTML = document.getElementById('message').innerHTML;
            var newHTML = oldHTML + '<br />' + evt.data;
            alert(oldHTML);
            alert(newHTML);
            document.getElementById('message').innerHTML=newHTML;
        };
        function onOpen(evt){
            websocket.send("Message to send");
        };
        function testWebSocket() { 
            websocket = new WebSocket(wsUri); 
            websocket.onopen = function(evt) { onOpen(evt) };
        //    websocket.onclose = function(evt) { onClose(evt) };
            websocket.onmessage = function(evt) { onMessage(evt) };
        //   websocket.onerror = function(evt) { onError(evt) }; 
        }
        window.addEventListener("load", init, false);
    </script>

