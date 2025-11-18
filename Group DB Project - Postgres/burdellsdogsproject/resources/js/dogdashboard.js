function toggleTable(input) {

    const all = document.getElementById('all');
    const adoptable = document.getElementById('adoptable');
    const unadoptable = document.getElementById('unadoptable');

    all.style.display = 'none';
    adoptable.style.display = 'none';
    unadoptable.style.display = 'none';

    if (input === 'all') {
        all.style.display = '';
    } else if (input === 'adoptable') {
        adoptable.style.display = '';
    } else if (input === 'unadoptable') {
        unadoptable.style.display = '';
    } else {
        all.style.display = '';
    }
    
}

// event listeners for filter options
document.addEventListener('DOMContentLoaded', function() {
    toggleTable('all');
    document.getElementById('allbutton').addEventListener('click', () => toggleTable('all'));
    document.getElementById('adoptablebutton').addEventListener('click', () => toggleTable('adoptable'));
    document.getElementById('unadoptablebutton').addEventListener('click', () => toggleTable('unadoptable'));
});

// event listeners for dogs
document.addEventListener('DOMContentLoaded', function() {
    const rows = document.querySelectorAll('.dogRow');
    
    rows.forEach(row => {
        row.addEventListener('click', function() {

            const dogId = this.getAttribute('data-dog');
            window.location.href = '/dogdetails/' + dogId;
        
        });
    });
});