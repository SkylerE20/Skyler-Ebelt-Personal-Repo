<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<meta http-equiv="X-UA-Compatible" content="ie=edge">
	<title>Burdell's Dogs</title>
</head>
<body>
	<h2>Add Dog Form</h2>

    @if(session('success'))
        <div style="color: green;">
            {{ session('success') }}
        </div>
    @endif
	@if(session('error'))
        <div style="color: red;">
            {{ session('error') }}
        </div>
    @endif
	@if ($errors->any())
		<div style="color: red;">
			<ul>
				@foreach ($errors->all() as $error)
					<li>{{ $error }}</li>
				@endforeach
			</ul>
		</div>
	@endif
    
	<form id="newDogForm" action="/addNewDog" method="POST">
		@csrf

		<label for="newName">Name:</label>
		<input type="text" id="newName" name="newName">
		<br/>
		<br/>

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
		
		<label for="newSex">Sex:</label>
		<select id="newSex" name="newSex">
			<option value="Unknown">Unknown</option>   
			<option value="Male">Male</option>
			<option value="Female">Female</option>
		</select>
		
		<br/>
		<br/>

		<label for="newAltered">Altered:</label>
		<input type="hidden" name="newAltered" value="false">
		<input type="checkbox" id="newAltered" name="newAltered" value="true">
		<br/>
		<br/>

		<label for="newAge">Age in Months:</label>
		<input type="number" id="newAge" name="newAge">
		<br/>
		<br/>

        <label for="newDescription">Description:</label>
        <textarea id="newDescription" name="newDescription" rows="4" cols="50"></textarea>
        <br/>
        <br/>

        <label for="microchipvendor">Microchip Vendor:</label>
        <select id="microchipvendor" name="newMicrochipVendor">
            <option value="">Select Vendor</option>
            @foreach ($microchipvendor as $vendor)
            <option value="{{ $vendor->vendor_name }}">{{ $vendor->vendor_name }}</option>
            @endforeach
        </select>
        
        <label for="mchipID">Microchip ID:</label>
        <input id="mchipID" id="newMicrochipID" name="newMicrochipID" type="text">
        <br/>
        <br/>

		<label for="newSurrenderDate">Surrender Date:</label>
		<input type="date" id="newSurrenderDate" name="newSurrenderDate">
		<br/>
		<br/>

		<label for="newSurrenderPhone">Surrender Phone Number:</label>
		<input type="text" id="newSurrenderPhone" name="newSurrenderPhone">
		<br/>
		<br/>

		<label for="newSurrenderByAnimalControl">Surrendered By Animal Control:</label>
        <input type="hidden" name="newSurrenderByAnimalControl" value="false">
		<input type="checkbox" id="newSurrenderByAnimalControl" name="newSurrenderByAnimalControl" value="true">
		<br/>
		<br/>

		<button type="submit">Add New Dog</button>
	</form>

    @vite(['resources/js/addnewdog.js'])
</body>
</html>