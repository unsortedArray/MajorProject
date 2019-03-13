window.addEventListener('load', function () {


	firebase.auth().onAuthStateChanged(function (user) {
        console.log("here");
		if (user) {
			var status = dataBaseHandler();
			console.log(user);
		} else {
			window.location = "index.html";
			Materialize.toast('user is logged out!', 3000, 'rounded', 'top');
		}
	});


});