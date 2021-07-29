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
  fetch("/add-like", {
    method: "POST",
    body: JSON.stringify({ recipe_id: recipe_id }),
  }).then((_res) => {
    window.location.reload(true);
  });
}

function addDislike(recipe_id) {
  fetch("/add-dislike", {
    method: "POST",
    body: JSON.stringify({ recipe_id: recipe_id }),
  }).then((_res) => {
    window.location.reload(true);
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

function deleteIngredient(ingredient_id) {
  if (confirm("Are you sure you want to delete this ingredient?"))
    fetch("/delete ingredient", {
      method: 'POST',
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
    body: JSON.stringify({ ingredient_id: ingredient_id, Dosage: x, UnitName: y, MyIngredient: z }),
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
  fetch("/Delete recipe", {
    
  }).then((_res) => {
    window.location.reload(true);
  });

}

function history_delete(id) {
if (confirm("Are you sure you want to delete this browsing history?"))
    fetch("/delete history", {
      method: 'POST',
      body: JSON.stringify({ id: id }),
    }).then((_res) => {
      window.location.reload(true);
    });
}

function deletedicription(id, step_no) {
  if (confirm("Are you sure you want to delete this dicription?"))
  fetch("/delete discription", {
    method: 'POST',
    body: JSON.stringify({ id: id, step_no: step_no}),
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

