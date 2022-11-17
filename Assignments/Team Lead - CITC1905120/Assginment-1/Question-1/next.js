window.addEventListener('load', () =>{

    const name = localStorage.getItem("NAME");
    const email = localStorage.getItem("MAIL_ID");
    const mobileNumber = localStorage.getItem("MOBILE_NUMBER");

    document.getElementById('name').innerHTML = name;
    document.getElementById('mailId').innerHTML = email;
    document.getElementById('mobileNumber').innerHTML = mobileNumber;

})