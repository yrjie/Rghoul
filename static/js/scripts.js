// Empty JS for your own code to be here
function like(picName){
		var cnt = document.getElementById("like_" + picName);
		var xmlHttp = new XMLHttpRequest();
	    xmlHttp.open( "GET", "/like/" + picName + "/", false );
	    xmlHttp.send( null );
	    if (xmlHttp.responseText.length<10)
	    	cnt.innerHTML = xmlHttp.responseText;
	}
	
function dislike(picName){
	var cnt = document.getElementById("dislike_" + picName);
	var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", "/dislike/" + picName + "/", false );
    xmlHttp.send( null );
    cnt.innerHTML = xmlHttp.responseText;
    if (xmlHttp.responseText.length<10)
    	cnt.innerHTML = xmlHttp.responseText;
}

function likeSp(picName){
        var cnt = document.getElementById("like_" + picName);
        var xmlHttp = new XMLHttpRequest();
        xmlHttp.open( "GET", "/likeSp/" + picName + "/", false );
        xmlHttp.send( null );
        if (xmlHttp.responseText.length<10)
            cnt.innerHTML = xmlHttp.responseText;
    }
    
function dislikeSp(picName){
    var cnt = document.getElementById("dislike_" + picName);
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", "/dislikeSp/" + picName + "/", false );
    xmlHttp.send( null );
    cnt.innerHTML = xmlHttp.responseText;
    if (xmlHttp.responseText.length<10)
        cnt.innerHTML = xmlHttp.responseText;
}