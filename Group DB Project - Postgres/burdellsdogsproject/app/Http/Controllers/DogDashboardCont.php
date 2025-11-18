<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class DogDashboardCont extends Controller
{
    public function showDogDashboard() {
          
        // calculate spots left
        $maxDogs = config('MaxDogs.MaxDogs');

        $numDogs = DB::selectOne(
            "SELECT (
                (SELECT COUNT(dog_ID) FROM dog) - 
                (SELECT COUNT(dog_ID) FROM adoptedrelation)
            ) AS num_dogs"
        )->num_dogs;

        $spotsLeft = $maxDogs - $numDogs;
        
        // pass in all 3 tables for filtered views
        $dogsInShelter = DB::select(
            "
            SELECT 
                d.dog_id,
                d.dog_name, 
                STRING_AGG(ib.breed_name, '/' ORDER BY ib.breed_name) AS breed_names, 
                d.sex, 
                d.altered, 
                d.age, 
                CASE 
                    WHEN mc.dog_id IS NULL OR d.altered IS FALSE
                    THEN 'Unadoptable' 
                    ELSE 'Adoptable' 
                END AS adoptability_status, 
                d.surrender_date 
            FROM Dog d 
            LEFT JOIN IsBreed ib ON d.dog_id = ib.dog_id 
            LEFT JOIN AdoptedRelation ar ON d.dog_id = ar.dog_id 
            LEFT JOIN Microchip mc ON d.dog_id = mc.dog_id
            WHERE ar.dog_id IS NULL
            GROUP BY d.dog_id, d.dog_name, d.sex, d.altered, d.age, d.surrender_date, ar.dog_id, mc.dog_id 
            ORDER BY d.surrender_date
            "
        );

        $dogsInShelterAdoptable = DB::select(
            "
            SELECT
                fd.dog_id,
                fd.dog_name,
                fd.breed_names,
                fd.sex,
                fd.altered,
                fd.age,
                fd.adoptability_status,
                fd.surrender_date
            FROM (
                SELECT 
                    d.dog_id,
                    d.dog_name, 
                    STRING_AGG(ib.breed_name, '/' ORDER BY ib.breed_name) AS breed_names, 
                    d.sex, 
                    d.altered, 
                    d.age, 
                    CASE 
                        WHEN mc.dog_id IS NULL OR d.altered IS FALSE
                        THEN 'Unadoptable' 
                        ELSE 'Adoptable' 
                    END AS adoptability_status, 
                    d.surrender_date 
                FROM Dog d 
                LEFT JOIN IsBreed ib ON d.dog_id = ib.dog_id 
                LEFT JOIN AdoptedRelation ar ON d.dog_id = ar.dog_id
                LEFT JOIN Microchip mc ON d.dog_id = mc.dog_id
                WHERE ar.dog_id IS NULL
                GROUP BY d.dog_id, d.dog_name, d.sex, d.altered, d.age, d.surrender_date, ar.dog_id, mc.dog_id 
                ORDER BY d.surrender_date)
            AS fd
            WHERE adoptability_status = 'Adoptable';
            "
        );

        $dogsInShelterUnadoptable = DB::select(
            "
            SELECT
                fd.dog_id,
                fd.dog_name,
                fd.breed_names,
                fd.sex,
                fd.altered,
                fd.age,
                fd.adoptability_status,
                fd.surrender_date
            FROM (
            SELECT 
                d.dog_id,
                d.dog_name, 
                STRING_AGG(ib.breed_name, '/' ORDER BY ib.breed_name) AS breed_names, 
                d.sex, 
                d.altered, 
                d.age, 
                CASE 
                    WHEN mc.dog_id IS NULL OR d.altered IS FALSE
                    THEN 'Unadoptable' 
                    ELSE 'Adoptable' 
                END AS adoptability_status, 
                d.surrender_date 
            FROM Dog d 
            LEFT JOIN IsBreed ib ON d.dog_id = ib.dog_id 
            LEFT JOIN AdoptedRelation ar ON d.dog_id = ar.dog_id 
            LEFT JOIN Microchip mc ON d.dog_id = mc.dog_id
            WHERE ar.dog_id IS NULL
            GROUP BY d.dog_id, d.dog_name, d.sex, d.altered, d.age, d.surrender_date, ar.dog_id, mc.dog_id 
            ORDER BY d.surrender_date)
            AS fd
            WHERE adoptability_status = 'Unadoptable';
            "
        );

        return view('dogdashboard', compact('spotsLeft', 'dogsInShelter', 'dogsInShelterAdoptable', 'dogsInShelterUnadoptable'));
    }
}
