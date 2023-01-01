const closebtn = document.getElementsByClassName("closebtn")[0];
const alertDiv = closebtn.parentElement;

closebtn.onclick = function () {
  setTimeout(function () {
    hideAlert();
  }, 600);
};

const hideAlert = () => {
  if (alertDiv.style.display === "block") {
    alertDiv.style.display = "none";
  }
};

const showAlert = () => {
  if (alertDiv.style.display === "none") {
    alertDiv.style.display = "block";
  }
  setTimeout(function () {
    hideAlert();
  }, 5000);
};
