<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Burdell's Dogs</title>
</head>
<style>
    table, th, td {
        border: 1px solid black;
        border-collapse: collapse;
        padding: 5px;
    }
    div {
        padding: 10px;
    }
    .dogRow {
        cursor: pointer;
    }
    .dogRow:hover {
        background-color: #f1f1f1;
    }
</style>
<body>
    <h2>Dog Dashboard</h2>
    <p>Spots Left in the Shelter: {{ $spotsLeft }}</p>

    <div>
        <button id='allbutton'>All Dogs</button>
        <button id='adoptablebutton'>Adoptable</button>
        <button id='unadoptablebutton'>Unadoptable</button>
    </div>

    <table id='all'>
        <th colspan="7">All Dogs</th>
        <tr>
            <th>Name</th>
            <th>Breed</th>
            <th>Sex</th>
            <th>Altered?</th>
            <th>Age (months)</th>
            <th>Status</th>
            <th>Surrender Date</th>
        </tr>
        @foreach ($dogsInShelter as $DDdog)
        <tr class="dogRow" data-dog="{{ $DDdog->dog_id }}">
            <td>{{ $DDdog->dog_name }}</td>
            <td>{{ $DDdog->breed_names }}</td>
            <td>{{ $DDdog->sex }}</td>
            <td>{{ $DDdog->altered ? 'true' : 'false' }}</td>
            <td>{{ $DDdog->age }}</td>
            <td>{{ $DDdog->adoptability_status }}</td>
            <td>{{ $DDdog->surrender_date }}</td>
        </tr>
        @endforeach
    
    </table>

    <table id='adoptable'>
        <th colspan="7">Adoptable Dogs</th>
        <tr>
            <th>Name</th>
            <th>Breed</th>
            <th>Sex</th>
            <th>Altered?</th>
            <th>Age (months)</th>
            <th>Status</th>
            <th>Surrender Date</th>
        </tr>
        @foreach ($dogsInShelterAdoptable as $DDdog)
        <tr class="dogRow" data-dog="{{ $DDdog->dog_id }}">
            <td>{{ $DDdog->dog_name }}</td>
            <td>{{ $DDdog->breed_names }}</td>
            <td>{{ $DDdog->sex }}</td>
            <td>{{ $DDdog->altered ? 'true' : 'false' }}</td>
            <td>{{ $DDdog->age }}</td>
            <td>{{ $DDdog->adoptability_status }}</td>
            <td>{{ $DDdog->surrender_date }}</td>
        </tr>
        @endforeach
    
    </table>

    <table id='unadoptable'>
        <th colspan="7">Unadoptable Dogs</th>
        <tr>
            <th>Name</th>
            <th>Breed</th>
            <th>Sex</th>
            <th>Altered?</th>
            <th>Age (months)</th>
            <th>Status</th>
            <th>Surrender Date</th>
        </tr>
        @foreach ($dogsInShelterUnadoptable as $DDdog)
        <tr class="dogRow" data-dog="{{ $DDdog->dog_id }}">
            <td>{{ $DDdog->dog_name }}</td>
            <td>{{ $DDdog->breed_names }}</td>
            <td>{{ $DDdog->sex }}</td>
            <td>{{ $DDdog->altered ? 'true' : 'false' }}</td>
            <td>{{ $DDdog->age }}</td>
            <td>{{ $DDdog->adoptability_status }}</td>
            <td>{{ $DDdog->surrender_date }}</td>
        </tr>
        @endforeach
    
    </table>
    <br>
    
    <div>
        @if ($spotsLeft < 1)
            <p>No Spots Left In Shelter</p>
        @endif
        <button onclick="window.location.href='/addNewDog'">Add Dog</button>
    </div>
    

    <div>
    <button id="addAdoptionButton" type="button" onclick="window.location.href='{{ route('applications.create') }}'">
        Add Adoption Application
    </button>
    </div>

    <div>
    <button id="processAdoptionButton" type="button" onclick="window.location.href='{{ route('adoptions.index') }}'">
        Process Adoption Application
    </button>
    </div>

    @if(session('isExec') === true)
        <h2>Reports</h2>
        <a href="/applications">View/Approve/Reject Adoption Application</a> <br>
        <a href="/reports/animal-control">Animal Control Report</a> <br>
        <a href="/MonthlyAdoption">Monthly Adoption Report</a> <br>
        <a href="/ExpenseAnalysis">Expense Analysis Report</a> <br>
        <a href="/VolunteerLookup">Volunteer Lookup Report</a> <br>
        <a href="/VolunteerBirthday">Volunteer Monthly Birthday Report</a> <br>
    @endif

    @vite(['resources/js/dogdashboard.js'])
</body>
</html>