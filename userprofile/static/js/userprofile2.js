
async function saveChanges() {
    

    var formData = new FormData(document.getElementById("edit-profile-form"));

    var username = formData.get('username');
    var email = formData.get('email');

  if (!username || !email) {
    // Jika input kosong, tampilkan pesan kesalahan atau lakukan tindakan sesuai kebutuhan
    showAlert("Please fill the form!", 'warning');
    return;
  }
    fetch("/userprofile/edit_profile_ajax", {
    method: "POST",
    body: formData,
  })
    .then(response => {
    response.json();
    showAlert('Username and Email Has Been Successfully Changed!','warning');
        }).catch(error => {
      // Tangani kesalahan jika fetch gagal
      
      // Kembalikan teks awal jika terjadi kesalahan
    });
    var linkElement2 = document.getElementById("usernametextprofiledetails");
    var linkElement3 = document.getElementById("useremailtextprofiledetails");
    linkElement2.textContent = document.getElementById('inputusername').value;
    linkElement3.textContent = document.getElementById('inputuseremail').value;
}


async function savePassword() {
    var formData = new FormData(document.getElementById("change-password-form"));
    var oldpassword = formData.get('old_password');
    var newpassword = formData.get('new_password1');
    var newpasswordconfirm = formData.get('new_password2')
    var error = false;
    if (!oldpassword || !newpassword || !newpasswordconfirm) {
    // Jika input kosong, tampilkan pesan kesalahan atau lakukan tindakan sesuai kebutuhan
    showAlert("Please fill the form!", 'warning');
    return;
  }
    if(newpassword != newpasswordconfirm) {
        showAlert('Wrong confirm Password','warning');
        return;
    }


    fetch("/userprofile/change_password_ajax", {
    method: "POST",
    body: formData,
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Password Error');
        }
        else {
            showAlert('Password Has Been Successfully Changed!','warning');
        }
        return response.text();
    })
    .then(data => {
        // Handle your successful response here
    })
    .catch(error => {
        if (error.message === 'Password Error') {
            showAlert('Change Password is not valid, read the rules','warning');
        }
    });


}

function showAlert(message, category) {
    var html = '<div class="alert alert-' + category + ' alert-dismissible fade show" role="alert">' +
        message +
        '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>' +
        '</div>';

    document.getElementById('alert_placeholder').innerHTML = html;
}



    