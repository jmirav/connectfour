$(document).ready(function() {
	window.ws = new WebSocket('ws://' + location.hostname + ':' +
                            location.port + location.pathname + '/ws');

	window.ws.onopen = function() {
    setupGame();
	};

	window.ws.onmessage = function(e) {
    message = JSON.parse(e.data);
    kind = message.kind;

    switch(kind) {
      case "game_started":
        resetBoard();
        disablePlayAgainButton();
        enablePlayButtons();
        updateGameNumber(message.game_number);
        break;

      case "next_player":
        updateFeedbackBar(message.player + "'s turn");
        break;

      case "color_played":
        updateGameSquare(message.color, message.position);

      case "try_again":
        updateFeedbackBar(message.player + " try again (" +
                          message.reason + ")");
        break;

      case "game_won":
        disablePlayButtons();
        updateFeedbackBar("Game won by " + message.player);
        enablePlayAgainButton()
        break;

      case "game_draw":
        disablePlayButtons();
        updateFeedbackBar("Game ended in a draw");
        enablePlayAgainButton()
        break;

      default:
        console.log(message);
    }
	};
});


function resetBoard() {
  $(".game-square").css("background", "yellow");
}


function updateGameSquare(color, position) {
  id = "#square-" + position[0] + "-" + position[1];
  $(id).css("background", color);
}


function updateFeedbackBar(message) {
  $("#game-feedback").text(message);
}


function updateGameNumber(number) {
  $("#game-number").text(number);
}


function enablePlayButtons() {
  $(".column-play").removeAttr("disabled");
}


function disablePlayButtons() {
  $(".column-play").attr("disabled", true);
}


function enablePlayAgainButton() {
  $("#play-again").removeAttr("disabled");
}


function disablePlayAgainButton() {
  $("#play-again").attr("disabled", true);
}


function setupGame() {
  sendCreateBoard(num_rows, num_columns, num_to_win);
  for (var i = 0; i < players.length; i++) {
    sendAddPlayer(players[i], colors[i]);
  }
  sendStartGame();
}


function sendAddPlayer(name, color) {
  window.ws.send(JSON.stringify({
    "kind": "add_player",
    "name": name,
    "color": color,
  }));
}


function sendCreateBoard(num_rows, num_columns, num_to_win) {
  window.ws.send(JSON.stringify({
    "kind": "create_board",
    "num_rows": num_rows,
    "num_columns": num_columns,
    "num_to_win": num_to_win,
  }));
}


function sendStartGame() {
  window.ws.send(JSON.stringify({
    "kind": "start_game",
  }));
}


function sendPlay(column) {
  window.ws.send(JSON.stringify({
    "kind": "play",
    "column": column,
  }));
}


function sendPrint(message) {
  window.ws.send(JSON.stringify({
    "kind": "print",
    "message": message,
  }));
}
