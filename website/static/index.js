function createComment2(recipe_id) {
  var new_comment = document.getElementById("comment_textarea").value;
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
  fetch("/subscribe-to-newsletters", {
    method: "POST",
    body: JSON.stringify(),
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
function deleteIngredient(ingredient_id) {
  if (confirm("Are you sure you want to delete this ingredient?"))
    fetch("/delete ingredient", {
      method: "POST",
      body: JSON.stringify({ ingredient_id: ingredient_id }),
    }).then((_res) => {
      window.location.reload(true);
    });
}

function modifyIngredient(ingredient_id, order) {
  var x = document.getElementsByName("dosage")[order].value;
  var y = document.getElementsByName("Unit Name")[order].value;
  var z = document.getElementsByName("Ingredient Name")[order].value;

  fetch("/modify ingredient", {
    method: "POST",
    body: JSON.stringify({
      ingredient_id: ingredient_id,
      Dosage: x,
      UnitName: y,
      MyIngredient: z,
    }),
  }).then((_res) => {
    window.location.reload(true);
  });
}

function AddIngredient() {
  var a = document.getElementsByName("number of dosage")[0].value;
  var b = document.getElementsByName("Unit")[0].value;
  var c = document.getElementsByName("Ingredient")[0].value;
  fetch("/push ingredient", {
    method: "POST",
    body: JSON.stringify({ Dosage: a, UnitName: b, MyIngredient: c }),
  }).then((_res) => {
    window.location.reload(true);
  });
}

function recipe_delete() {
  if (confirm("Are you sure you want to delete this recipe?"))
    fetch("/Delete recipe", {}).then((_res) => {
      window.location.reload(true);
    });
}

function history_delete(id) {
  if (confirm("Are you sure you want to delete this browsing history?"))
    fetch("/delete history", {
      method: "POST",
      body: JSON.stringify({ id: id }),
    }).then((_res) => {
      window.location.reload(true);
    });
}

function deletedicription(id, step_no) {
  if (confirm("Are you sure you want to delete this dicription?"))
  fetch("/delete discription", {
    method: "POST",
    body: JSON.stringify({ id: id, step_no: step_no }),
  }).then((_res) => {
    window.location.reload(true);
  });
}

function trending_filter() {
  var filter = document.getElementsByName("filter")[0].value;
  fetch("/Trending filter", {
    method: "POST",
    body: JSON.stringify({ filter: filter}),
  }).then((_res) => {
    window.location.reload(true);
  });

}

