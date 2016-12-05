var playernum = 0;
var room = 0;
window.onload = function() {
  room = prompt("Please enter your room number!");
  console.log(room);

  postPlayerNum("/newroom", "room=" + room);
  document.getElementById('rock').addEventListener("click", function() {
    postRequestURL("/reply", "room=" + room + "&player=" + playernum + "&item=1");
  });
  document.getElementById('paper').addEventListener("click", function() {
    postRequestURL("/reply", "room=" + room + "&player=" + playernum + "&item=2");
  });
  document.getElementById('scissor').addEventListener("click", function() {
    postRequestURL("/reply", "room=" + room + "&player=" + playernum + "&item=3");
  });

  setInterval(function () {
    postWinner("/update", "room=" + room + "&player=" + playernum);
  }, 1000);
};

window.onbeforeunload = function () {
    postRequestURL("/playerleaves", "room=" + room + "&player=" + playernum);
};

function postPlayerNum(url, body) {
  url = 'http://' + document.location.hostname + ':' + document.location.port + url
  var xhr = new XMLHttpRequest();
  xhr.open('POST', url, true);
  xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
  //'room=1234&player=1&item=0'
  xhr.send(body);
  var result = "";
  xhr.onload = function () {
    // do something to response
    if (xhr.readyState === 4) {
      if (xhr.status === 200) {
        result = xhr.responseText;
        console.log(result.split("="));
        playernum = result.split("=")[1];
        if(playernum == -1){
          document.getElementById('playernum').innerHTML = "Room is full!";
        } else {
          document.getElementById('playernum').innerHTML = "You are player: " + playernum;
        }
      }
    }
  };
};

function postWinner(url, body) {
  url = 'http://' + document.location.hostname + ':' + document.location.port + url
  var xhr = new XMLHttpRequest();
  xhr.open('POST', url, true);
  xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
  //'room=1234&player=1&item=0'
  xhr.send(body);
  var result = "";
  xhr.onload = function () {
    // do something to response
    if (xhr.readyState === 4) {
      if (xhr.status === 200) {
        result = xhr.responseText;
        console.log(result.split("="));
        winnernum = result.split("=")[1];
        if(winnernum != 0 && winnernum !== undefined){
          document.getElementById('winner').innerHTML = "The Winner: " + winnernum;
        }
      }
    }
  };
};


function postRequestURL(url, body) {
  url = 'http://' + document.location.hostname + ':' + document.location.port + url
  var xhr = new XMLHttpRequest();
  xhr.open('POST', url, true);
  xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
  //'room=1234&player=1&item=0'
  xhr.send(body);
  var result = "";
  xhr.onload = function () {
    // do something to response
    if (xhr.readyState === 4) {
      if (xhr.status === 200) {
        result = xhr.responseText;
        console.log(result);
        return result;
      }
    }
  };
};
