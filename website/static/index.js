function onSignIn(googleUser) {
  var profile = googleUser.getBasicProfile();
  console.log("ID: " + profile.getId()); // Do not send to your backend! Use an ID token instead.
  console.log("Name: " + profile.getName());
  console.log("Image URL: " + profile.getImageUrl());
  console.log("Email: " + profile.getEmail()); // This is null if the 'email' scope is not present.
}

function signOut() {
  var auth2 = gapi.auth2.getAuthInstance();
  auth2.signOut().then(function () {
    console.log("User signed out.");
  });
}

function create_book() {
  var txt;
  var name = prompt("CookBook Name：", "NewBook");
  if (name == null || name == "") {
      txt = "cancel";
  } else {
      txt = "Hello，" + name + "！How r u？";
      fetch("/cookbook", {
        method: "POST",
        body: JSON.stringify({
          name: txt,
        }),
      }).then((_res) => {
        window.location.reload(true);
      });
  }
}


function createComment2(recipe_id) {
  var new_comment = prompt("Create a new comment on this recipe.");
  if (new_comment != null) {
    fetch("/create-comment", {
      method: "POST",
      body: JSON.stringify({
        recipe_id: recipe_id,
        comment: new_comment,
      }),
    }).then((_res) => {
      window.location.reload(true);
    });
  }
}

function deleteComment(comment_id) {
  if (confirm("Are you sure you want to delete this comment?"))
    fetch("/delete-comment", {
      method: "POST",
      body: JSON.stringify({ comment_id: comment_id }),
    }).then((_res) => {
      window.location.reload(true);
    });
}

function modifyComment(comment_id) {
  var new_comment = prompt("Enter new comment to change.");
  if (new_comment != null) {
    fetch("/modify-comment", {
      method: "POST",
      body: JSON.stringify({ comment_id: comment_id, comment: new_comment }),
    }).then((_res) => {
      window.location.reload(true);
    });
  }
}

function addLike(recipe_id) {

  
  $.ajax({
    type : "POST", // http method
    url : "http://127.0.0.1:5000/add-like", // the endpoint
    data : {id: JSON.parse( recipe_id )
    }, // data sent with the post request

    // handle a successful response
    success : function() {
        console.log("success"); // another sanity check
    },

    // handle a non-successful response
    error : function(xhr,errmsg,err) {
        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
    }
});

}

function addDislike(recipe_id) {
  $.ajax({
    type : "POST", // http method
    url : "http://127.0.0.1:5000/add-dislike", // the endpoint
    data : {id: JSON.parse( recipe_id )
    }, // data sent with the post request

    // handle a successful response
    success : function() {
        console.log("success"); // another sanity check
    },

    // handle a non-successful response
    error : function(xhr,errmsg,err) {
        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
    }
});
}

function unsubscribeToNewsletters() {
  if (confirm("Are you sure you want to unsubscribe from this service?"))
    fetch("/unsubscribe-to-newsletters", {
      method: "POST",
    }).then((_res) => {
      window.location.reload(true);
    });
}

/*Onclick method that gets selected checkboxes and sends it 
  back into subscribe-to-newsletter as a post method */
function subscribeToNewsletters() {
  var inputs = document.getElementsByName("checkbox");
  var selected = [];
  for (var i = 0; i < inputs.length; i++) {
    if (inputs[i].checked) {
      selected.push(inputs[i].value);
    }
  }

  fetch("/subscribe-to-newsletters", {
    method: "POST",
    body: JSON.stringify({ checkboxes: selected }),
  }).then((_res) => {
    window.location.reload(true);
  });
}

// Update Like count and the colour of the like icon in the recipe page
function updateLike(num_of_likes, num_of_dislikes, like_status) {
  console.log(document.getElementById("arrow-up").style.color)
  if (document.getElementById("dislike").innerHTML > num_of_dislikes) {
      if (document.getElementById("like").innerHTML == num_of_likes) {
        document.getElementById("like").innerHTML = num_of_likes+1;          
      } else {
        document.getElementById("like").innerHTML = num_of_likes
      }
      document.getElementById("dislike").innerHTML = num_of_dislikes;
  } else if (document.getElementById("dislike").innerHTML < num_of_dislikes) 
      if (document.getElementById("like").innerHTML == num_of_likes) {
        document.getElementById("like").innerHTML = num_of_likes+1;
      } else {
        document.getElementById("like").innerHTML = num_of_likes
      }

  else if (document.getElementById("like").innerHTML > num_of_likes) 
    document.getElementById("like").innerHTML = num_of_likes;
  else if (document.getElementById("like").innerHTML < num_of_likes) {
    document.getElementById("like").innerHTML = num_of_likes;
  } else {

    if (like_status == 1) 
      document.getElementById("like").innerHTML = num_of_likes-1;
    else if (like_status == 0)
      document.getElementById("like").innerHTML = num_of_likes+1;
    else {
      document.getElementById("like").innerHTML = num_of_likes+1;
      document.getElementById("dislike").innerHTML = num_of_dislikes-1;
    }

  }
  // Change colour of text
  document.getElementById("dislike").style.color = "darkgray";
  document.getElementById("arrow-down").style.color = "";
  if (document.getElementById("like").style.color == "darkgray") {  
    document.getElementById("like").style.color = "darkorange";
    document.getElementById("arrow-up").style.color = "darkorange";
  } else {
    document.getElementById("like").style.color = "darkgray";
    document.getElementById("arrow-up").style.color = "";
  }

}


// Update Disike count and the colour of the dislike icon in the recipe page
function updateDislike(num_of_likes, num_of_dislikes, like_status) {
  if (document.getElementById("like").innerHTML > num_of_likes) {
      if (document.getElementById("dislike").innerHTML == num_of_dislikes) 
        document.getElementById("dislike").innerHTML = num_of_dislikes+1;  
      else 
        document.getElementById("dislike").innerHTML = num_of_dislikes
      document.getElementById("like").innerHTML = num_of_likes;
  } else if (document.getElementById("like").innerHTML < num_of_likes) 
      if (document.getElementById("dislike").innerHTML == num_of_dislikes) 
        document.getElementById("dislike").innerHTML = num_of_dislikes+1;  
      else 
        document.getElementById("dislike").innerHTML = num_of_dislikes
          
  else if (document.getElementById("dislike").innerHTML > num_of_dislikes) 
    document.getElementById("dislike").innerHTML = num_of_dislikes;
  else if (document.getElementById("dislike").innerHTML < num_of_dislikes) {

    document.getElementById("dislike").innerHTML = num_of_dislikes;
  } else {        

    if (like_status == -1) 
      document.getElementById("dislike").innerHTML = num_of_dislikes-1;
    else if (like_status == 0)
      document.getElementById("dislike").innerHTML = num_of_dislikes+1;
    else {
      document.getElementById("like").innerHTML = num_of_likes-1;
      document.getElementById("dislike").innerHTML = num_of_dislikes+1;
    }
  }
  // Change colour of text
  document.getElementById("like").style.color = "darkgray";
  document.getElementById("arrow-up").style.color = "";
  if (document.getElementById("dislike").style.color == "darkgray") {  
    document.getElementById("dislike").style.color = "darkorange";
    document.getElementById("arrow-down").style.color = "darkorange";
  } else {
    document.getElementById("dislike").style.color = "darkgray";
    document.getElementById("arrow-down").style.color = "";
  }
}
