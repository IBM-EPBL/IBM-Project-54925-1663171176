
function handleSubmit(){

    const name = document.getElementById('User_Name').value;
    const mail = document.getElementById('Email_Id').value;
    const mobileNumber = document.getElementById('Mobile_Number').value;

    localStorage.setItem("NAME", name);
    localStorage.setItem("MAIL_ID", mail);
    localStorage.setItem("MOBILE_NUMBER", mobileNumber);

    return;
} 