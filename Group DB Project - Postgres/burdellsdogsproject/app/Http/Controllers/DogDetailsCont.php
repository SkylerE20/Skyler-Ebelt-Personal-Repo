<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class DogDetailsCont extends Controller
{
    public function index() {
        $dogs = DB::select("SELECT dog_id, dog_name FROM dog;");
        return view('dogdetails', ['dogs' => $dogs]);
    }

    public function showDogDetails(Request $request) {
        $dogId = (int) $request->route('dog_id');
    
        $query = "
        SELECT
            d.dog_id AS dogId,  
            d.dog_name AS Name, 
            STRING_AGG(ib.breed_name, '/' ORDER BY ib.breed_name) AS Breed, 
            d.sex AS Sex, 
            d.altered AS Alteration_Status, 
            d.age AS Age, 
            d.description AS description,
            CASE  
                WHEN ar.dog_id IS NOT NULL
                THEN 'Already Adopted'
                WHEN m.dog_id IS NULL OR d.altered IS FALSE
                THEN 'Unadoptable'
                ELSE 'Adoptable' 
            END AS Adoptability_Status,  
            COALESCE(m.microchip_id::VARCHAR, 'Not Available') AS Microchip_ID, 
            d.surrender_date AS Surrender_Date, 
            COALESCE(d.surrenderer_phone_number, 'Not Available') AS Surrenderer_Phone_Number, 
            d.surrendered_by_animal_control AS Surrendered_By_Animal_Control 
        FROM Dog d 
        LEFT JOIN IsBreed ib ON d.dog_id = ib.dog_id 
        LEFT JOIN AdoptedRelation ar ON d.dog_id = ar.dog_id 
        LEFT JOIN Microchip m ON d.dog_id = m.dog_id 
        WHERE d.dog_id = ?
        GROUP BY d.dog_id, d.dog_name, d.sex, d.altered, d.age, d.surrender_date, ar.dog_id, m.microchip_id, d.surrenderer_phone_number, d.surrendered_by_animal_control;
        ";

        $dogDetail = DB::selectOne($query, [$dogId]);
        
        $dogs = DB::select("SELECT dog_id, dog_name FROM dog;"); 

        $breeds = DB::select("SELECT breed_name FROM breed;");

        $thisBreeds = DB::select(
            "
            SELECT breed_name
            FROM isbreed
            WHERE dog_id = ?
            "
        , [$dogId]);

        $microchipvendor = DB::select("SELECT vendor_name FROM microchipvendor");

        $volEmail = session('email_address');

        $volAge = DB::selectOne(
            "
            SELECT EXTRACT(YEAR FROM AGE(birth_date)) AS age
            FROM volunteer
            WHERE email_address = ?
            "
        , [$volEmail]);

        //expenses section

        $expenseTable = DB::select(
            "
            SELECT
                e.category_name,
                SUM(e.cost) AS total_category_expense
            FROM Expense e
            WHERE e.dog_id = ?
            GROUP BY e.category_name
            ORDER BY e.category_name;
            "
        ,[$dogId]
        );

        $grandTotal = DB::selectOne(
            "
            SELECT
            SUM(e.cost) AS total_expense
            FROM Expense e
            WHERE e.dog_id = ?
            "
        ,[$dogId]
        );
        
        return view('dogdetails', compact('dogs', 'dogDetail', 'breeds','microchipvendor', 'thisBreeds', 'volAge', 'expenseTable', 'grandTotal'));
    }

    public function updateDogDetail(Request $request) {
        $dogId = (int) $request->route('dog_id');

        $validated = $request->validate([
            'newBreed' => 'nullable|array',
            'newSex'  => 'nullable',
            'newAltered' => 'nullable',
            'newMicrochipVendor' => 'nullable',
            'newMicrochipID' => 'nullable'
        ]);
    
        $newBreed = $validated['newBreed'] ?? null;
            if (!is_null($newBreed)) {
            DB::delete('DELETE FROM isbreed WHERE dog_id = ?', [$dogId]);
            foreach ($newBreed as $breed) {
                DB::insert('INSERT INTO isbreed VALUES (?, ?)', [$dogId, $breed]);
            }
        }

        $newSex = $validated['newSex'] ?? null;
        if (!is_null($newSex)) {
            DB::update('UPDATE dog SET sex = ? WHERE dog_id = ?', [$newSex, $dogId]);
        }

        $newAltered = $validated['newAltered'] ?? null;
        if (!is_null($newAltered)) {
            DB::update('UPDATE dog SET altered = ? WHERE dog_id = ?', [$newAltered, $dogId]);
        }

        if (!empty($validated['newMicrochipVendor']) && !empty($validated['newMicrochipID'])) {
            $newMicrochipVendor = $validated['newMicrochipVendor'];
            $newMicrochipID = $validated['newMicrochipID'];
            DB::insert(
            "
            INSERT INTO microchip 
            VALUES (?, ?, ?)
            ", [$newMicrochipID, $dogId, $newMicrochipVendor]);
        }
    
        return redirect()->back()->with('success', 'Dog name updated successfully');
    }
    
    
}
