window.onload = function() {
  var room = prompt("Please enter your room number!");
  console.log(room);

  var player = postRequestURL("/newroom", "room=" + room);
  var playernum = player.split("=")[1];
  document.getElementById('playernum').innerHTML = "You are player: " + playernum;

  setInterval(function () {
    var winner = postRequestURL("/update", "room=" + room + "&player=" + playernum);
    var winnernum = player.split("=")[1];
    if(winnernum != 0 && winnernum !== undefined){
      document.getElementById('winner').innerHTML = "The Winner: " + winnernum;
    }
  }, 100);

  document.getElementById('rock').addEventListener("click", function() {
    postRequestURL("/reply", "room=" + room + "&player=" + playernum + "&item=1");
  });
  document.getElementById('rock').addEventListener("click", function() {
    postRequestURL("/reply", "room=" + room + "&player=" + playernum + "&item=2");
  });
  document.getElementById('rock').addEventListener("click", function() {
    postRequestURL("/reply", "room=" + room + "&player=" + playernum + "&item=3");
  });

}

window.onbeforeunload = function () {
    postRequestURL("/playerleaves", "room=" + room + "&player=" + playernum);
};

function postRequestURL(url, body) {
  url = 'http://localhost:8888' + url
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
      }
    }
  };
  return result;
}
