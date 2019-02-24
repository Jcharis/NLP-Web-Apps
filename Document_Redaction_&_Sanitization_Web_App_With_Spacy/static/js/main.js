function copyToClipboard(element) {
  var $temp = $("<input>");
  $("body").append($temp);
  $temp.val($(element).text()).select();
  document.execCommand("copy");
  alert("Result Copied");
  $temp.remove();
}

// function copyToClipboard() {
//   var copyText = document.getElementById("p1");
//   copyText.select();
//   document.execCommand("copy");
//   alert("Copied the result ");
//   console.log("Copied");
// }