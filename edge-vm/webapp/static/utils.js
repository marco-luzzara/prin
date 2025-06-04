function showMsg(msgDiv, text, type) {
    msgDiv.textContent = text;
    msgDiv.className = `message ${type}`;

    setTimeout(() => {
        msgDiv.textContent = ''
        msgDiv.className = 'message';
    }, 10000)
}

function addFileUploadSubmitListener(form, submitBtn, apiEndpoint, fileInput, msgDiv) {
    form.addEventListener('submit', function (event) {
        event.preventDefault();
        submitBtn.disabled = true;

        if (fileInput.files.length === 0) {
            showMsg(msgDiv, 'Non hai caricato alcun file', 'error');
            return;
        }

        const file = fileInput.files[0];
        if (!file.name.match(/\.(xls|xlsx|odt)$/)) {
            showMsg(msgDiv, 'Il tipo di file non è valido. File compatibili: .xls,.xlsx,.odt', 'error');
            return;
        }

        const formData = new FormData();
        formData.append('data_file', file);

        fetch(apiEndpoint, {
            method: 'POST',
            body: formData
        })
            .then(res => {
                console.log(res);

                if (res.ok) {
                    showMsg(msgDiv, 'File caricato correttamente', 'success');
                }
                else {
                    throw new Error(`The response returned status ${res.status}`);
                }
            })
            .catch(error => {
                showMsg(msgDiv, 'Si è verificato un errore', 'error');
                console.error(error);
            })
            .then(_ => {
                submitBtn.disabled = false;
                fileInput.value = ''
            });
    });
}