document.addEventListener("DOMContentLoaded", function () {
  // const controller = new AbortController()
  // const signal = controller.signal
  // document
  //   .querySelector("#djangoAllPosts")
  //   .addEventListener("click", () => loadAllPosts());
  // document
  //   .querySelector(".navbar-brand")
  //   .addEventListener("click", () => loadAllPosts());
  //TODO: Event listener for the Post button.  Update to go to function.
  //FIXME: Enable this again when you want to product JSON for a new Post.
  // document.querySelector("#post-button").addEventListener("click", (event) => {
  //   event.preventDefault();
  //   savePost();
  // });
  // document.querySelector("[id^='editButton']").addEventListener("click", (event) => {
  //   event.preventDefault();
  //   editPost(post.content, post.id);
  // });

  //Only disable the new post button if it exists.  This will throw an error otherwise.
  let element = document.querySelector("#post-body");

  if (element != null) {
    // Do something with the element
    disableNewPostButton();
  }
});

function loadAllPosts() {
  //window.location.href = "post";
  // document.querySelector("#post-view").style.display = "block";
  //FIXME: Only use this to return JSON as an API.  Not currently used for anything.

  fetch(`/posts`)
    .then((response) => response.json())
    .then((posts) => {
      // TODO: this finally works!

      console.log(posts); //
      myJSONArray = posts;

      let counter = 0;

      for (let i = 0; i < myJSONArray.length; i++) {
        let obj = myJSONArray[i];
        // postDiv = document.createElement("div");
        // postDiv.className = "post" + counter;

        // document.querySelector("#allPostings").append(postDiv);

        // //create p within the div for
        // creator = document.createElement("h5");
        // creator.className = "creator";
        // creator.innerHTML = obj.creator;
        // document.querySelector(".post" + counter).append(creator);

        //FIXME: create it as readonly.
        //create p within the div for the content
        // content = document.createElement("textarea");
        // content.className = "form-control content" + counter;
        // content.id = "readonlyContent" + counter;
        // content.innerHTML = obj.content;
        // document.querySelector(".post" + counter).append(content);

        //FIXME: need to put this where the user clicks the edit Post button.
        // var button = document.createElement("button");

        // button.innerHTML = "Edit post";
        // button.className = "btn btn-sm btn-outline-primary edit" + counter;
        document.querySelector(".post" + counter).append(button);

        editButton = document.getElementsByClassName(button.className);
        editButton[0].addEventListener("click", (event) => {
          // event.preventDefault();
          editPost(obj.content, obj.id);
        });

        //create p within the div for the subject
        // timestamp = document.createElement("p");
        // timestamp.className = "timestamp" + counter;
        // timestamp.innerHTML = obj.createdDate;
        // document.querySelector(".post" + counter).append(timestamp);

        //create p within the div for the subject
        // likes = document.createElement("p");
        // likes.className = "numberLikes" + counter;
        // likes.innerHTML = obj.numberLikes;
        // document.querySelector(".post" + counter).append(likes);

        // Need to update stylesheet here.  Flag to mark email as read.

        counter++;
      }

      //Check that the text area exists.
      // const textarea = document.querySelectorAll("[id^='readonly']");
      // //Returns an HTML collection.  Need the first in the list.
      // console.log(textarea); // null

      let count = 0;

      // for (let i = 0; i < textarea.length; i++) {
      //   //Set the text area to read only before the user edits.  Also change the number
      //   //of rows.
      //   document.getElementById("readonlyContent" + `${count}`).readOnly = true;
      //   document.getElementById("readonlyContent" + `${count}`).rows = "5";

      //   count++;
      // }

      return false;
    });
}

//FIXME: need to get the CSRF token here to do a POST.

function editPost(postID) {
  // This is the edit button that was clicked on.

  //FIXME: need to send the Postcontent and the ID from the event listener.
  const element = event.target;
  //Post div class name.
  buttonParentClassName = element.parentElement.className;
  //class  of the button that was clicked.
  buttonClass = element.className;

  //Select the button first.
  postdiv = document.getElementsByClassName(buttonClass);
  console.log(postdiv[0]);
  test = postdiv[0].className;

  //last char of each of the elements.
  const lastChar = test.substring(test.length - 1);

  //existing content text area class name.
  const textAreaClassRemove = "content" + lastChar;

  //create the new element.
  //TODO: update this to have a full form, div, text area and save button in it.  Do it in the
  //innerHTML

  // newItem = document.createElement("div");
  //FIXME: May need to change the method to "POST".  Need to add an event listener to the button to save the post.

  // newItem.innerHTML = `<form action="" method="POST" class="editForm" id=editForm>  <textarea name="" id="editTextArea"
  // class="form-control editTextArea" rows=5>${postContent}</textarea><input type="submit" value="Save post"
  // class="btn btn-sm btn-outline-primary SavePostButton"></form>`;

  //FIXME: This just replaced the button with the text above.  Need to replace
  //the entire div.  Needs to be specific to Posts only.  Only replace the button if
  // it starts with a specific name that
  // test = postdiv.className;
  // console.log(test);

  //const editFormClassName = "editForm";

  const editForm = "editForm" + lastChar;
  //This unhides the form for editing the post and the save button.
  document.getElementById(editForm).className = "editForm";

  // FIXME: need to set the value of the

  const readOnlyContent = "#" + "readonlyContent" + lastChar;
  //Get the value of the text area before it is hidden.
  const originalText = document.querySelector(readOnlyContent).value;

  //Set the original value in the text area.
  const TextArea = "textArea" + lastChar;
  document.getElementById(TextArea).value = originalText;

  //hide the read only text area and edit post button
  //hide the text  area.

  const readonly = "readonlyContent" + lastChar;

  document.getElementById(readonly).className = "hidden";

  //hide the button
  const editButton = "editButton" + lastChar;
  document.getElementById(editButton).className = "hidden";

  //FIXME: The SavePost button does not exist at this point?
  //Add an event listener for the Save post button.
  //   savePostbutton[0].addEventListener("click", () =>
  //   saveEditedPost(postID)
  // );

  // savePostbutton.addEventListener("click", () => saveEditedPost(postID));

  const savePostbutton = "#" + "savePostButton" + lastChar;

  document
    .querySelector(savePostbutton)
    .addEventListener("click", () =>
      saveEditedPost(postID, lastChar, originalText)
    );

  //FIXME: Need to add the original content back to the editable text area.

  //Change the button.
  // postdiv[0].parentNode.replaceChild(newItem, postdiv[0]);

  //remove the readonly textare for  existing content for the post.
  //FIXME: rather than remove here, just make it hidden.

  // document
  //   .querySelector(`[class$=${CSS.escape(textAreaClassRemove)}]`)
  //   .remove();

  //Check that the button exists.
  // const btn = document.getElementsByClassName(
  //   "btn btn-sm btn-outline-primary SavePostButton"
  // );
  //Returns an HTML collection.  Need the first in the list.
  // console.log(btn); // null

  // savePostbutton = document.getElementsByClassName(
  //   "btn btn-sm btn-outline-primary SavePostButton"
  // );
  //Add an event listener for the Save post button.
  // savePostbutton[0].addEventListener("click", () =>
  //   saveEditedPost(postContent, postID)
  // );

  //return false;
}

//FIXME: need to get the CSRF token here to do a PUT, it will not show an error.  Rigth now I have set it to exempt in the python view.
//This is currently what I'm using to update the text area without refreshing.
//This sends to updatePost route in Django
function saveEditedPost(postID, lastChar, originalText) {
  console.log("I'm in the SaveEdited Post function!");
  // console.log(postContent);
  console.log(postID);
  console.log(lastChar);

  textAreaContentUpdate = document.querySelector("#textArea" + lastChar).value;

  const formControl = "form-control content" + lastChar;
  //readonly area to reenable:
  document.getElementById("readonlyContent" + lastChar).className = formControl;

  //This is hard-coded, what does it do?  perhaps  delete.
  //FIXME:

  const editButton = "btn btn-sm btn-outline-primary edit" + lastChar;
  document.getElementById("editButton" + lastChar).className = editButton;

  //Get the updated value.
  document.querySelector("#" + "readonlyContent" + lastChar).value =
    textAreaContentUpdate;

  document.getElementById("textArea" + lastChar).className = "hidden";

  document.getElementById("savePostButton" + lastChar).className = "hidden";

  // test = getCookie("csrftoken")
  // getCookie("csrftoken")

  //Get the cookie so the application is secure.
  csrfCookie = getCookie("csrftoken");

  fetch(`/posts/${postID}`, {
    method: "PUT",
    headers: { "Content-type": "application/json", "X-CSRFToken": csrfCookie },
    body: JSON.stringify({
      content: textAreaContentUpdate,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      console.log("I'm here.");

      test2 = data.responseCode;

      //This is no longer necessary since I validate the front end for empty posts.
      if (test2 === "400") {
        console.log("400code");
        //the user didn't enter any text.  If the user gets this error.  the readonly area will
        //have to be re-populated with the text that was submitted.  Pop an alert here.
        alert("Empty posts are not permitted.  Please try again.");
        //Need to add this back to teh form.
        console.log(originalText);

        const readOnlyContent = "#" + "readonlyContent" + lastChar;
        //Get the value of the text area before it is hidden.
        document.querySelector(readOnlyContent).value = originalText;
      }

      // if(!response.ok) {
      //   return response.text().then(text => { throw new Error(text) })
      //  }

      // const readonly = "readonlyContent" + lastChar;

      // newClassName = "form-control content" + lastChar;

      // document.getElementById(readonly).className = newClassName;

      //reinstate the button
      // const editButton = "editButton" + lastChar;
      // clssName = "btn btn-sm btn-outline-primary edit" + lastChar;
      // document.getElementById(editButton).className = clssName;

      const editForm = "editForm" + lastChar;
      // Need to set the savePost form text area and button class to hidden
      // again, so that it  can be reset.
      document.getElementById(editForm).className = "hidden";

      //Set the original value in the text area.
      const TextArea = "textArea" + lastChar;
      document.getElementById(TextArea).value = textAreaContentUpdate;

      document.getElementById("textArea" + lastChar).className =
        "form-control editTextArea";

      const savePostbutton =
        "btn btn-sm btn-outline-primary SavePostButton" + lastChar;

      document.getElementById("savePostButton" + lastChar).className =
        savePostbutton;

      return false;
      // event.preventDefault();
    });

  // .catch((error) => {
  //   console.log(error);
  // });

  return false;

  // return false;
  // event.preventDefault()

  //FIXME: Do I need to add an event listener for the edit post button again.
  // document.getElementById("editButton" + lastChar).className =
  // "btn btn-sm btn-outline-primary edit0";

  // document.querySelector("[id^='editButton0']").addEventListener("click", (event) => {
  //   event.preventDefault();
  //   debugger;
  //   editPost(postID);
  // });

  //FIXME: Need to put this back the way it was.

  // const editForm = "editForm" + lastChar;
  //Need to set the savePost form text area and button class to hidden
  // again, so that it  can be reset.
  // document.getElementById(editForm).className = "hidden";

  //Set the original value in the text area.
  // const TextArea = "textArea" + lastChar;
  // document.getElementById(TextArea).value = originalText;

  // document.getElementById("textArea" + lastChar).className = "form-control editTextArea";

  // const savePostbutton = "savePostButton" + lastChar;

  // const readonly = "readonlyContent" + lastChar;

  // newClassName = "form-control content" + lastChar;

  // document.getElementById(readonly).className = newClassName;

  // //reinstate the button
  // const editButton = "editButton" + lastChar;
  // clssName = "btn btn-sm btn-outline-primary edit" + lastChar;
  // document.getElementById(editButton).className = clssName;
}

//This for creating a new post.  This goes to savePost view in Django.
function savePost() {
  console.log("I'm in the savePost function!");

  //Get the cookie so the application is secure.
  csrfCookie = getCookie("csrftoken");

  fetch("/post", {
    method: "POST",
    headers: { "Content-type": "application/json", "X-CSRFToken": csrfCookie },
    body: JSON.stringify({
      content: document.querySelector("#post-body").value,
    }),
  })
    .then((response) => response.json())
    .then((result) => {
      // Print result
      console.log(result);
    });

  //timeout so that database is updated.
  // setTimeout(() => {
  //   loadAllPosts();
  //   console.log("Delayed for 100 milliseconds.");
  // }, "100");
}

//likely only need postID and currentUser here because Like button is filtered out if the creator of post and current user are the
//same.
//This is the handler for both like and unLike.
function likePost(postID, creatorOfPost, currentUser) {
  console.log("In Like Post function!");
  console.log(postID);
  console.log(currentUser);
  console.log(creatorOfPost);

  // This is the edit button that was clicked on.

  //FIXME: need to send the Postcontent and the ID from the event listener.
  const element = event.target;
  //Post div class name.
  likeIconClassName = element.parentElement.className;
  //class  of the button that was clicked.
  likeIconClass = element.className;

  //This finds the class name of the like/unlike icon.
  postdiv = document.getElementsByClassName(likeIconClass);
  //This is what needs to change to hidden later.
  classNameLikeIcon = postdiv[0].className;
  console.log(classNameLikeIcon);

  //last char of each of the elements.
  const lastChar = classNameLikeIcon.substring(classNameLikeIcon.length - 1);

  const substrthumbsUp = "thumbs-up";
  const substrthumbsDown = "thumbs-down";

  console.log(classNameLikeIcon.includes(substrthumbsUp));
  console.log(classNameLikeIcon.includes(substrthumbsDown));

  //Get the cookie so the application is secure.
  csrfCookie = getCookie("csrftoken");

  if (classNameLikeIcon.includes(substrthumbsUp)) {
    // If the icon is thumbs up, Go to the unlike function and remove the like.
    fetch(`/unlikePost/${postID}`, {
      method: "PUT",
      headers: {
        "Content-type": "application/json",
        "X-CSRFToken": csrfCookie,
      },
      body: JSON.stringify({
        creator: creatorOfPost,
        currentUser: currentUser,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        console.log("Just finished fetching unlike information.");

        //Get the number of likes to add to the page.
        numberLikes = data["data"];

        //Need to hide the existing thumbs up and display the thumbs down and also update the count with the numberLikes.

        //Hide the thumbs up icon
        const thumbsUpID = "thumbsUp" + lastChar;
        document.getElementById(thumbsUpID).className = "hidden";

        //Unhide the thumbs down icon
        const thumbDownID = "thumbsDown" + lastChar;
        const classNameThumbsDown = "fa fa-thumbs-down " + lastChar;
        document.getElementById(thumbDownID).className = classNameThumbsDown;

        const likeID = "numberLikes" + lastChar;
        document.getElementById(likeID).innerHTML =
          "<strong>Number of likes</strong>: " + numberLikes;

        return false;
      });

    return false;
  } else {
    //If the icon is thumbs down, Go to the like function and add the like.

    fetch(`/likePost/${postID}`, {
      method: "PUT",
      headers: {
        "Content-type": "application/json",
        "X-CSRFToken": csrfCookie,
      },
      body: JSON.stringify({
        creator: creatorOfPost,
        currentUser: currentUser,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        console.log("Just finished fetching Like information.");

        //Get the number of likes to add to the page.
        numberLikes = data["data"];

        //Hide the thumbs Down icon
        const thumbsUpID = "thumbsDown" + lastChar;
        document.getElementById(thumbsUpID).className = "hidden";

        //Unhide the thumbs Up icon
        const thumbUpID = "thumbsUp" + lastChar;
        const classNameThumbsUp = "fa fa-thumbs-up " + lastChar;
        document.getElementById(thumbUpID).className = classNameThumbsUp;

        const likeID = "numberLikes" + lastChar;
        document.getElementById(likeID).innerHTML =
          "<strong>Number of likes</strong>: " + numberLikes;

        return false;
      });
  }
}

function followUnfollowUser(currentUserProfile, loggedinUser) {
  console.log("In followUnfollowUser function!");
  //The user for which we are displaying the profile
  console.log(currentUserProfile);
  //The user that is currently logged in.
  console.log(loggedinUser);

  const element = event.target;

  //likeIconClassName = element.parentElement.className;
  //class  of the button that was clicked.
  followUnfollowClass = element.className;

  //Look for the "Unfollow" substring in the class name.
  const str = followUnfollowClass;
  const substr = "unfollow";

  //Get the cookie so the application is secure.
  csrfCookie = getCookie("csrftoken");

  if (str.includes(substr)) {
    console.log("Clicked Unfollow!");
    //remove the user as a follower.

    //const follow = false;

    fetch(`/followUser/${currentUserProfile}`, {
      method: "PUT",
      headers: {
        "Content-type": "application/json",
        "X-CSRFToken": csrfCookie,
      },
      body: JSON.stringify({
        currentUser: currentUserProfile,
        follow: false,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        console.log("Just finished fetching the information.");

        //Need to hide the existing button and display the hidden Follow button.

        document.getElementById("unfollowButton").className = "hidden";

        document.getElementById("followButton").className =
          "btn btn-sm btn-outline-primary follow";

        //Display the "no longer following" heading.

        debugger;

        document.getElementById("text_nofollowing_top").className = "hidden"

        document.getElementById("text_nofollowing_bottom").className = "text_nofollowing_bottom"

        return false;
      });
  } else {
    console.log("Clicked Follow!");
    //add the user as a follower.

    fetch(`/followUser/${currentUserProfile}`, {
      method: "PUT",
      headers: {
        "Content-type": "application/json",
        "X-CSRFToken": csrfCookie,
      },
      body: JSON.stringify({
        currentUser: currentUserProfile,
        follow: true,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);

        console.log("Just finished fetching the information.");

        //Need to hide the existing button and display the hidden Unfollow button.
        document.getElementById("followButton").className = "hidden";
        document.getElementById("unfollowButton").className =
          "btn btn-sm btn-outline-primary unfollow";

              //Display the "no longer following" heading.

        debugger;

        document.getElementById("text_following_top").className = "hidden"

        document.getElementById("text_following_bottom").className = "text_following_bottom"

        return false;
      });
  }
}

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
}

function disableNewPostButton() {
  if (document.getElementById("post-body").value === "") {
    document.getElementById("post-button").disabled = true;
  } else {
    document.getElementById("post-button").disabled = false;
  }
}

function disableEditPostButton(counter) {
  const textAreaID = "textArea" + counter;
  const buttonID = "savePostButton" + counter;
  if (document.getElementById(textAreaID).value === "") {
    document.getElementById(buttonID).disabled = true;
  } else {
    document.getElementById(buttonID).disabled = false;
  }
}
