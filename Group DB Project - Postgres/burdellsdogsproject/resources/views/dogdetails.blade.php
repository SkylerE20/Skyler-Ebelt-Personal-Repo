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
</style>
<body>
    <form id="dogForm">
        <select id="dogSelector" onchange="fetchDogDetails()">
            <option value="">Select a Dog</option>
            @foreach ($dogs as $dogTemp)
                <option value="{{ $dogTemp->dog_id }}">{{ $dogTemp->dog_name }}</option>
            @endforeach
        </select>
    </form>

    @if (session('success'))
        <div style="color: green;">
            {{ session('success') }}
        </div>
    @endif
    
    <div id="dogDetail">
        @if (isset($dogDetail))
            <h2>Details for: {{ $dogDetail->name }}</h2>
            <p>Breeds:</p>
            <ul>
                @foreach($thisBreeds as $breed)
                    <li>{{ $breed->breed_name }}</li>
                @endforeach
            </ul>
            <p>Sex: {{ $dogDetail->sex }}</p>
            <p>Altered?: {{ $dogDetail->alteration_status ? 'true' : 'false' }}</p>
            <p>Age in Months: {{ $dogDetail->age }}</p>
            <p>Adoptability Status: {{ $dogDetail->adoptability_status }}</p>
            <p>Description: {{ $dogDetail->description }}</p>
            <p>Microchip ID: {{ $dogDetail->microchip_id }}</p>
            <p>Surrender Date: {{ $dogDetail->surrender_date }}</p>
            <p>Surrenderer Phone Number: {{ $dogDetail->surrenderer_phone_number }}</p>
            <p>Surrendered By Animal Control: {{ $dogDetail->surrendered_by_animal_control }}</p>
            <p>Dog ID: {{ $dogDetail->dogid }}</p>
        @else
            <p>Please select a dog to see the details.</p>
        @endif
    </div>

    <div id="updateForm" style="display:none;">
        <h2>Details for: {{ $dogDetail->name }}</h2>
        <form action="/dogdetails/{{$dogDetail->dogid}}" method="POST">
            @csrf

            @if(collect($thisBreeds)->contains(function ($breed) {
                return $breed->breed_name === "Mixed" || $breed->breed_name === "Unknown";
            }))
                <label for="breedSelector">Breed:</label>
                <select id="breedSelector" name="newBreed[]" multiple>
                    @foreach ($breeds as $breed)
                        <option value="{{ $breed->breed_name }}">
                            {{ $breed->breed_name }}
                        </option>
                    @endforeach
                </select>
                <br>
                <br>
            @else
                <p>Breeds:</p>
                <ul>
                    @foreach($thisBreeds as $breed)
                        <li>{{ $breed->breed_name }}</li>
                    @endforeach
                </ul>
            @endif
            
            @if($dogDetail->sex === "Unknown")
                <label for="sexSelector">Sex:</label>
                <select id="sexSelector" name="newSex">   
                    <option value="Male">Male</option>
                    <option value="Female">Female</option>
                </select>
            @else
                <p>Sex: {{ $dogDetail->sex }}</p>
            @endif

            @if($dogDetail->alteration_status === 0)
                <label for="altered">Altered:</label>
                <input type="checkbox" id="altered" name="newAltered">
            @else
                <p>Altered?: {{ $dogDetail->alteration_status ? 'true' : 'false' }}</p>
            @endif

            <p>Age in Months: {{ $dogDetail->age }}</p>
            <p>Adoptability Status: {{ $dogDetail->adoptability_status }}</p>
            <p>Description: {{ $dogDetail->description }}</p>


            @if ($volAge->age < 18)
                <p>Microchip ID: {{ $dogDetail->microchip_id }}</p>
                <p style="color: red;">Must be over 18 to edit this field</p>
            @else
                @if ($dogDetail->microchip_id === 'Not Available')
                    <label for="microchipvendor">Microchip Vendor:</label>
                    <select id="microchipvendor" name="newMicrochipVendor">
                        <option value="">Select Vendor</option>
                        @foreach ($microchipvendor as $vendor)
                        <option value="{{ $vendor->vendor_name }}">{{ $vendor->vendor_name }}</option>
                        @endforeach
                    </select>
                    <label for="mchipID">Microchip ID:</label>
                    <input id="mchipID" name="newMicrochipID" type="text">
                @else
                    <p>Microchip ID: {{ $dogDetail->microchip_id }}</p>
                @endif
            @endif

            <p>Surrender Date: {{ $dogDetail->surrender_date }}</p>
            <p>Surrenderer Phone Number: {{ $dogDetail->surrenderer_phone_number }}</p>
            <p>Surrendered By Animal Control: {{ $dogDetail->surrendered_by_animal_control }}</p>
            <p>Dog ID: {{ $dogDetail->dogid }}</p>

            <button type="submit">Submit</button>
            <br>
            <br>
        </form>

    </div>
    <button id='editbutton'>Edit</button>

    <h2>Expenses</h2>


    <table id='expenseTable'>
        <tr>
            <th>Category</th>
            <th>Expenses</th>
        </tr>
        @foreach ($expenseTable as $categoryRow)
            <tr>
                <td>{{ $categoryRow->category_name }}</td>
                <td>${{ number_format($categoryRow->total_category_expense, 2) }}</td>
            </tr>
        @endforeach
        <tr>
            <td><b>Total</b></td>
            <td>${{ number_format($grandTotal->total_expense, 2) }}</td>
        </tr>

    </table>
    <br>

    @if ($volAge->age < 18)
        <button id='fakeexpensebutton'>Add Expense</button>
        <p style="color: red;">Must be over 18 to add expenses</p>
    @else
        <button id="processAdoptionButton" type="button" onclick="window.location.href='/expenseForm/{{ $dogDetail->dogid }}'">
            Add Expense
        </button>
    @endif

    @vite(['resources/js/dogdetail.js'])

</body>
</html>






