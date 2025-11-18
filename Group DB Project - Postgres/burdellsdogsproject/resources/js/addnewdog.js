document.addEventListener('DOMContentLoaded', function() {
    const newdogform = document.getElementById('newDogForm');
    const surrenderPhone = document.getElementById('newSurrenderPhone');
    const surrenderAnimalControl = document.getElementById('newSurrenderByAnimalControl');
  
    if (newdogform) {
        newdogform.addEventListener('submit', function(event) {
            if (surrenderAnimalControl.checked && !surrenderPhone.value.trim()) {
                alert('Surrenders need a Surrender Phone Number.');
                event.preventDefault();
            }

            if (document.getElementById('newName').value === 'Uga') {
                const breeds = document.getElementById('breedSelector');
                const thisBreeds = Array.from(breeds.selectedOptions).map(option => option.value);
            
                if (thisBreeds.includes('Bulldog')) {
                    alert('Uga is an invalid name for a bulldog. Go Yellow Jackets :)');
                    event.preventDefault();
                }
            }

        });
    }
});