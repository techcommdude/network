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

  //FIXME: trying to get the class name of the div for editing the post.
  //Put this elsewhere.  Needs to be specific to the Edit button on the Posts.
  // document.addEventListener("click", (event) => {
  //   // Find what was clicked on
  //   // const element = event.target;
  //   // postClassName = element.parentElement.className;
  //   // debugger;
  //   event.preventDefault();
  //   editPost();
  // });

  //TODO: this needs to be done after all the posts are loaded.
  // debugger;
  // var items = document.querySelectorAll('[class*="btn btn-sm btn-outline-primary"]');
  // console.log(items)

  //TODO: Event listener for the Post button.  Update to go to function.
  document.querySelector("#post-button").addEventListener("click", (event) => {
    event.preventDefault();
    loadAllPosts();
  });

  document
    .querySelector("#following")
    .addEventListener("click", () => loadFollowing());

  // By default, load the profile for the user
  loadAllPosts();
});

function loadAllPosts() {
  document.querySelector("#post-view").style.display = "block";
  document.querySelector("#following-view").style.display = "none";
  document.querySelector("#profile-view").style.display = "none";
  document.getElementById("allPostings").innerHTML = "";

  //debugger;

  //TODO: Load all the existing posts.

  //TODO: Do not save if the post is empty?  Throw an error.

  //TODO: Clear out what is there after you Post it.

  //TODO: Add an event listener for the Post button.  Do it above.

  fetch(`/posts`)
    .then((response) => response.json())
    .then((posts) => {
      // TODO: this finally works!
      myJSONArray = JSON.parse(posts);
      // test = myJSONArray[0]["content"];
      // console.log(test);

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

        //TODO: create the button here.
        var button = document.createElement("button");

        button.innerHTML = "Edit post";
        button.className = "btn btn-sm btn-outline-primary edit" + counter;
        // button.onclick = () => {
        //   alert("here be dragons"); return false;
        // };
        document.querySelector(".post" + counter).append(button);

        //create p within the div for the subject
        content = document.createElement("p");
        content.className = "content";
        content.innerHTML = obj.content;
        document.querySelector(".post" + counter).append(content);

        //create p within the div for the subject
        timestamp = document.createElement("p");
        timestamp.className = "timestamp";
        timestamp.innerHTML = obj.createdDate;
        document.querySelector(".post" + counter).append(timestamp);

        //create p within the div for the subject
        likes = document.createElement("p");
        likes.className = "numberLikes";
        likes.innerHTML = obj.numberLikes;
        document.querySelector(".post" + counter).append(likes);

        // Need to update stylesheet here.  Flag to mark email as read.

        counter++;
      }
      //TODO: select all the Edit buttons.
      // debugger;
      // var items = document.querySelectorAll(
      //   '[class*="btn btn-sm btn-outline-primary"]'
      // );
      // console.log(items);

      //TODO: event listener for Edit buttons. call the editPost function after clicking.
      document.addEventListener("click", (event) => {
        // Find what was clicked on with a regular expression, test that it was the edit button, otherwise do nothing and continue.
        const element = event.target;
        const string = "^btn btn-sm btn-outline-primary edit";
        const regexp = new RegExp(string);
        if (regexp.test(element.className) === true) {
          //Name of the post div class.
          postClassName = element.parentElement.className;

          event.preventDefault();

          editPost();
        }
      });

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
  // debugger;
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

function editPost(post_id) {
  debugger;
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
  newItem = document.createElement("p");
  newItem.innerHTML = "blah";
  //FIXME: This just replaced the button with the text above.  Need to replace
  //the entire div.  Needs to be specific to Posts only.  Only replace the button if
  // it starts with a specific name that
  postdiv[0].parentNode.replaceChild(newItem, postdiv[0]);
  // element.parentElement.remove();
  debugger;
}

// return false;
