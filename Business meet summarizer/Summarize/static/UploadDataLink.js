const preSubmit = (data) => {
    var reader = new window.FileReader();
    reader.readAsDataURL(data);
    reader.onloadend = function() {
        base64 = reader.result;
        base64_str.value = base64.split(',')[1];
    }
}
