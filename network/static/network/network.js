document.addEventListener("DOMContentLoaded", function () {
  // Use buttons to toggle between views

  document
    .querySelector("#allPosts")
    .addEventListener("click", () => loadAllPosts());

  document
    .querySelector(".navbar-brand")
    .addEventListener("click", () => loadAllPosts());

  document.querySelector("#profile").addEventListener("click", (event) => {
    event.preventDefault();

    loadProfile();
  });

  //TODO: Event listener for the Post button.  Update to go to function.
  document.querySelector("#post-button").addEventListener("click", (event) => {
    event.preventDefault();
    loadAllPosts();
  });

  document
    .querySelector("#following")
    .addEventListener("click", () => loadFollowing());

  //timeout so that database is updated.
  setTimeout(() => {
    load_mailbox("sent");
    console.log("Delayed for 100 milliseconds.");
  }, "100");

  // By default, load the profile for the user
  loadAllPosts();
});

function loadAllPosts() {
  document.querySelector("#post-view").style.display = "block";
  document.querySelector("#following-view").style.display = "none";
  document.querySelector("#profile-view").style.display = "none";
  document.getElementById("allPostings").innerHTML = "";

  fetch(`/posts`)
    .then((response) => response.json())
    .then((posts) => {
      // TODO: this finally works!
      myJSONArray = JSON.parse(posts);

      let counter = 0;

      for (let i = 0; i < myJSONArray.length; i++) {
        let obj = myJSONArray[i];
        postDiv = document.createElement("div");
        postDiv.className = "post" + counter;

        document.querySelector("#allPostings").append(postDiv);

        //create p within the div for
        creator = document.createElement("h5");
        creator.className = "creator";
        creator.innerHTML = obj.creator;
        document.querySelector(".post" + counter).append(creator);

        //FIXME: create it as readonly.
        //create p within the div for the content
        content = document.createElement("p");
        content.className = "content" + counter;
        content.innerHTML = obj.content;
        document.querySelector(".post" + counter).append(content);
        //document.getElementsByClassName(content.className).readOnly = true;

        //Check that the text area exists.
        const btn = document.getElementsByClassName(`content.className`);
        //Returns an HTML collection.  Need the first in the list.
        console.log(btn); // null

        //Check that the h5 exists.
        const h5 = document.getElementsByClassName(`creator.className`);
        //Returns an HTML collection.  Need the first in the list.
        console.log(h5); // null

        //TODO: create the button here.
        var button = document.createElement("button");

        button.innerHTML = "Edit post";
        button.className = "btn btn-sm btn-outline-primary edit" + counter;
        document.querySelector(".post" + counter).append(button);

        editButton = document.getElementsByClassName(button.className);
        editButton[0].addEventListener("click", (event) => {
          // event.preventDefault();
          editPost(obj.content, obj.id);
        });

        //create p within the div for the subject
        timestamp = document.createElement("p");
        timestamp.className = "timestamp" + counter;
        timestamp.innerHTML = obj.createdDate;
        document.querySelector(".post" + counter).append(timestamp);

        //create p within the div for the subject
        likes = document.createElement("p");
        likes.className = "numberLikes" + counter;
        likes.innerHTML = obj.numberLikes;
        document.querySelector(".post" + counter).append(likes);

        // Need to update stylesheet here.  Flag to mark email as read.

        counter++;
      }

      return false;
    });
}

function loadFollowing() {
  document.querySelector("#post-view").style.display = "none";
  document.querySelector("#following-view").style.display = "block";
  document.querySelector("#profile-view").style.display = "none";
  document.getElementById("followingView").innerHTML = "";

  fetch(`/following`)
    .then((response) => response.json())
    .then((following) => {
      // Print email
      console.log(following);
    });

  return false;
}

function loadProfile() {
  document.querySelector("#post-view").style.display = "none";
  document.querySelector("#following-view").style.display = "none";
  document.querySelector("#profile-view").style.display = "block";
  document.getElementById("#profile-view").innerHTML = "";

  fetch(`/profile`)
    .then((response) => response.json())
    .then((profile) => {
      // Print email
      console.log(profile);
    });

  return false;
}

//FIXME: need to get the CSRF token here to do a POST.

function editPost(postContent, postID) {
  // This is the edit button that was clicked on.
  const element = event.target;
  //Post div class name.
  buttonParentClassName = element.parentElement.className;
  //class  of the button that was clicked.
  buttonClass = element.className;

  //Select the button first.
  postdiv = document.getElementsByClassName(buttonClass);
  console.log(postdiv[0]);
  //create the new element.
  //TODO: update this to have a full form, div, text area and save button in it.  Do it in the
  //innerHTML
  newItem = document.createElement("div");
  //FIXME: May need to change the method to "POST".  Need to add an event listener to the button to save the post.
  newItem.innerHTML = `<form action="" method="POST">  <textarea name="" id="editTextArea"
  class="form-control editTextArea" rows=5>${postContent}</textarea><input type="submit" value="Save post"
  class="btn btn-sm btn-outline-primary SavePostButton"></form>`;
  //FIXME: This just replaced the button with the text above.  Need to replace
  //the entire div.  Needs to be specific to Posts only.  Only replace the button if
  // it starts with a specific name that
  postdiv[0].parentNode.replaceChild(newItem, postdiv[0]);

  //TODO: remove the existing content for the post.
  document.querySelector("[class^='content']").remove();

  //Check that the button exists.
  const btn = document.getElementsByClassName(
    "btn btn-sm btn-outline-primary SavePostButton"
  );
  //Returns an HTML collection.  Need the first in the list.
  console.log(btn); // null

  savePostbutton = document.getElementsByClassName(
    "btn btn-sm btn-outline-primary SavePostButton"
  );
  //Add an event listener for the Save post button.
  savePostbutton[0].addEventListener("click", () =>
    saveEditedPost(postContent, postID)
  );

  return false;
}

//FIXME: need to get the CSRF token here to do a PUT, it will not show an error.  Rigth now I have set it to exempt in the python view.
function saveEditedPost(postContent, postID) {
  console.log("I'm in the SaveEdited Post!");
  console.log(postContent);
  console.log(postID);

  textAreaContentUpdate = document.querySelector("#editTextArea").value;

  fetch(`/posts/${postID}`, {
    method: "PUT",
    body: JSON.stringify({
      content: textAreaContentUpdate,
    }),
  });
}
