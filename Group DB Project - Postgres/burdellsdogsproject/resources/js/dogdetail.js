
function fetchDogDetails() {
    const dogId = document.getElementById('dogSelector').value;
    if (dogId) {
        window.location.href = `/dogdetails/${dogId}`;
    }
}

function toggleUpdateForm() {
    const dogDetail = document.getElementById('dogDetail');
    const updateForm = document.getElementById('updateForm');

    if (dogDetail.style.display == 'none') {
        dogDetail.style.display = 'block';
        updateForm.style.display = 'none';
    } else {
        dogDetail.style.display = 'none';
        updateForm.style.display = 'block';
    }
}

// event listeners for buttons
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('editbutton').addEventListener('click', () => toggleUpdateForm());
});