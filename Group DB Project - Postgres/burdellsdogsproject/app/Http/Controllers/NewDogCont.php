<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class NewDogCont extends Controller
{
    public function volunteerEmails() {
        $breeds = DB::select("SELECT breed_name FROM breed;");
        $microchipvendor = DB::select("SELECT vendor_name FROM microchipvendor");
        return view('AddNewDog', compact('breeds', 'microchipvendor'));
    }

    public function addNewDog(Request $request) {
      
        $validated = $request->validate([
            'newName' => 'required|string|max:249',
            'newBreed' => 'required|array', 
            'newSex'  => 'required',
            'newAge' =>  'required',
            'newDescription' => 'nullable|string|max: 499',
            'newMicrochipVendor' => 'nullable',
            'newMicrochipID' => 'nullable',
            'newSurrenderDate' => 'required|date|before:now',
            'newSurrenderPhone' => 'nullable|string|max: 19',
            'newAltered' => 'required',
            'newSurrenderByAnimalControl' => 'required'
        ]);
    
        $newName = $validated['newName'];

        $newSex = $validated['newSex'];

        $newAge = $validated['newAge'];

        $newAltered = $validated['newAltered'];

        $newSurrenderDate = $validated['newSurrenderDate'];

        $newSurrenderPhone = $validated['newSurrenderPhone'];

        $newSurrenderByAnimalControl = $validated['newSurrenderByAnimalControl'];

        $newVolunteerEmail = session('email_address');

        $newDescription = $validated['newDescription'];

        // calculate spots left
        $maxDogs = config('MaxDogs.MaxDogs');

        $numDogs = DB::selectOne(
            "SELECT (
                (SELECT COUNT(dog_ID) FROM dog) - 
                (SELECT COUNT(dog_ID) FROM adoptedrelation)
            ) AS num_dogs"
        )->num_dogs;

        $spotsLeft = $maxDogs - $numDogs;

        if ($spotsLeft < 0) {
            return redirect()->back()->with('error', 'Could not add dog, no spots left.')->withInput();
        }
        
        // insert dog into db
        DB::insert(
            '
            INSERT INTO dog (
                dog_name, 
                sex, 
                altered, 
                age, 
                surrender_date, 
                surrenderer_phone_number, 
                surrendered_by_animal_control, 
                volunteer_email, 
                description) 
            VALUES (?,?,?,?,?,?,?,?,?)
            ', 
            [$newName, 
            $newSex, 
            $newAltered, 
            $newAge, 
            $newSurrenderDate, 
            $newSurrenderPhone, 
            $newSurrenderByAnimalControl, 
            $newVolunteerEmail, 
            $newDescription]
        );

        // get the id of the inserted dog
        $lastId = DB::getPdo()->lastInsertId();

        // insert breed
        $newBreed = $validated['newBreed'] ?? null;
        foreach ($newBreed as $breed) {
            DB::insert('INSERT INTO isbreed VALUES (?, ?)', [$lastId, $breed]);
        }

        // insert chip, can only be done when both are present
        if (!empty($validated['newMicrochipVendor']) && !empty($validated['newMicrochipID'])) {
            $newMicrochipVendor = $validated['newMicrochipVendor'];
            $newMicrochipID = $validated['newMicrochipID'];
            DB::insert(
            "
            INSERT INTO microchip 
            VALUES (?, ?, ?)
            ", [$newMicrochipID, $lastId, $newMicrochipVendor]);
        }
    
        return redirect()->back()->with('success', 'New dog added successfully');
    }
    
}
