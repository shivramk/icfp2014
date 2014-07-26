
function load() {
    // Set globals
    broken = true
    //$("#break").unbind().html("Run").attr("id", "runAll")
    //$("#runAll").click(run)
    //var lambdaman = $("#lambda").val()
    //var map = $("#map").val()
    //var ghosts = $(".g").map(function () { return this.value }).get()
    state = loadGame(map, lambdaman, ghosts)
    if (state.error != null) {
        updateStatus("Error: " + state.error)
    }
    else {
        //$(".run").removeAttr("disabled")
        //$("#trace").empty()
        //$("#status").empty()
        //setupBoard()
        //updateStatus("Program Loaded")
        //updateBoard(true)
        updateState()
    }
}

function stepProg(o) {
    h$runSync(h$c2(h$ap1_e
                   , h$mainZCMainzigameStepWrapper
                   , h$c1(h$ghcjszmprimZCGHCJSziPrimziJSRef_con_e, o)
                   )
             , false
             );
}

function loadGame(gameBoard, lmanProg, gs) {
    var o = { gameboard: gameBoard, lmanprog: lmanProg, ghostprogs: gs };

    h$runSync(h$c2(h$ap1_e
                   , h$mainZCMainziloadGameWrapper
                   , h$c1(h$ghcjszmprimZCGHCJSziPrimziJSRef_con_e, o)
                   )
             , false
             );
    return o;
}

function runStep() {
    stepProg(state)
    if (state.gameOver == true) {
        breakRun()
        victor = state.gameWin ? "You won" : "You lost"
        //$(".run").attr("disabled", "disabled")
        updateState()
        //updateBoard(false)
        updateStatus("Game Over: " + victor)
    }
    else {
        //TODO: To print status at every step
        //updateState()
        //updateBoard(false)
    }
}

function run() {
    broken = false
    //$("#runAll").html("Break").unbind().attr("id", "break")
    //$("#break").click(breakRun)
    updateStatus("Game running")
    runLoop()
}

function runLoop() {
    while (!broken) {
        runStep()
        //setTimeout(runLoop, 0)
        //runLoop();
    }
}
function breakRun() {
    broken = true
    //$("#break").unbind().html("Run").attr("id", "runAll")
    //updateStatus("Broken by user")
    //updateState()
    //$("#runAll").click(run)
}


function updateState() {
    //$("#lives").html(state.lives)
    //$("#ticks").html(state.ticks)
    //$("#score").html(state.score)
    console.log("lives: " + state.lives + ", ticks: " + state.ticks + ", score: " + state.score);
    if (state.traceval != null) {
        for (var index = 0; index < state.traceval.length; ++index) {
            output(state.traceval[index]);
        }
    }
}
function updateStatus(status) {
    console.log(status)
}
