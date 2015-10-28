exports = exports ? this

# vars to setup
ws_uri = "ws://localhost:8080/ws"
realm = "realm1"
chan = "chan1"

# globals
g_session = null
cstatus_elm = null
chan1_rslt_elm = null
to_pub_elm = null

get_elements = ->
    # get dom elements by name
    console.log("get elements")
    cstatus_elm = document.getElementById("cstatus")
    chan1_rslt_elm = document.getElementById("chan1_result")
    to_pub_elm = document.getElementById("to_pub")
    
init_elements = ->
    # init status values
    console.log("init elements")
    cstatus_elm.textContent = "?"
    chan1_rslt_elm.textContent = "?"
    to_pub_elm.value = ""

pub_chan1 = ->
    pub_val = to_pub_elm.value
    console.log("shall pub #{pub_val}")
    g_session.publish(chan, [pub_val])



console.log("uri = #{ws_uri}")


setup_connection = ->
    console.log("setup connection")
    get_elements()
    init_elements()
    connection = new autobahn.Connection({url: ws_uri, realm: realm})
    g_connection = connection
    console.log("made connection")
    connection.onclose = (reason, details) =>
        console.log("close: #{reason}")
    console.log("declared onclose")
    
    connection.onopen = (session, details) =>
        console.log("conn.onopen")
        g_session = session
        on_msg = (args) ->
            console.log("on_msg callback #{args}")
            chan1_rslt_elm.textContent = args
        #console.log("declared on msg")

        cstatus_elm.value = "connected to #{ws_uri}"

        session.subscribe(chan, on_msg)
        #console.log("subsed 1")
        console.log("end of on_open")
    

        ##session.call(chan, [ ts, offset ]).then(
        ##    (res) ->
        ##        console.log("got result #{res.state}")
        ##        if res.state == 'ok'
        ##            console.log("good result")
        ##            populate_telep_state(res.telep)
        ##        console.log(res)
        ##        g_fetched_state = true
        ##)
        ##console.log("called")
    console.log("declared onopen")

    console.log("will open now")
    connection.open()


exports.pubsub = 
    setup_connection : setup_connection
    pub : pub_chan1
