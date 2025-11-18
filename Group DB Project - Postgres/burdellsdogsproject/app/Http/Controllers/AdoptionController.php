<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Carbon\Carbon;

class AdoptionController extends Controller
{
    public function index()
    {
        return view('adoptions.index');
    }
    
    public function searchApplications(Request $request)
    {
        $lastName = $request->input('last_name');
        
        $applications = DB::select("
            SELECT a.applicant_email, a.application_date, ad.first_name, ad.last_name, 
                   ad.applicant_phone, ad.household_size, ad.state_abbrev, ad.city, 
                   ad.street, ad.zip_code, aa.accept_date
            FROM approvedapplication aa
            JOIN application a ON aa.applicant_email = a.applicant_email AND aa.application_date = a.application_date
            JOIN adopter ad ON a.applicant_email = ad.applicant_email
            WHERE LOWER(ad.last_name) LIKE LOWER(?)
            ORDER BY aa.accept_date DESC
        ", ['%' . $lastName . '%']);
        
        return view('adoptions.search_results', ['applications' => $applications]);
    }
    
    public function selectDog($email, $date)
    {
        $applicant = DB::selectOne("
            SELECT a.applicant_email, a.application_date, ad.first_name, ad.last_name, 
                   ad.applicant_phone, ad.household_size, ad.state_abbrev, ad.city, 
                   ad.street, ad.zip_code, aa.accept_date
            FROM approvedapplication aa
            JOIN application a ON aa.applicant_email = a.applicant_email AND aa.application_date = a.application_date
            JOIN adopter ad ON a.applicant_email = ad.applicant_email
            WHERE a.applicant_email = ? AND a.application_date = ?
        ", [$email, $date]);
        
        if (!$applicant) {
            return redirect()->route('adoptions.index')
                ->withErrors(['error' => 'Approved application not found']);
        }
        
        $dogs = DB::select("
            SELECT d.dog_id, d.dog_name, d.sex, d.altered, d.age, d.description, 
                   d.surrender_date, d.surrendered_by_animal_control,
                   STRING_AGG(b.breed_name, ', ') as breeds
            FROM dog d
            LEFT JOIN isbreed ib ON d.dog_id = ib.dog_id
            LEFT JOIN breed b ON ib.breed_name = b.breed_name
            WHERE d.dog_id NOT IN (SELECT dog_id FROM adoptedrelation)
            GROUP BY d.dog_id, d.dog_name, d.sex, d.altered, d.age, d.description, 
                     d.surrender_date, d.surrendered_by_animal_control
            ORDER BY d.surrender_date
        ");
        
        return view('adoptions.select_dog', [
            'applicant' => $applicant,
            'dogs' => $dogs
        ]);
    }
    public function confirmAdoption($email, $date, $dogId)
    {
        $applicant = DB::selectOne("
            SELECT a.applicant_email, a.application_date, ad.first_name, ad.last_name, 
                   ad.applicant_phone, ad.household_size, ad.state_abbrev, ad.city, 
                   ad.street, ad.zip_code, aa.accept_date
            FROM approvedapplication aa
            JOIN application a ON aa.applicant_email = a.applicant_email AND aa.application_date = a.application_date
            JOIN adopter ad ON a.applicant_email = ad.applicant_email
            WHERE a.applicant_email = ? AND a.application_date = ?
        ", [$email, $date]);
        
        if (!$applicant) {
            return redirect()->route('adoptions.index')
                ->withErrors(['error' => 'Approved application not found']);
        }
        
        $dog = DB::selectOne("
            SELECT d.dog_id, d.dog_name, d.sex, d.altered, d.age, d.description, 
                   d.surrender_date, d.surrendered_by_animal_control,
                   STRING_AGG(b.breed_name, ', ') as breeds
            FROM dog d
            LEFT JOIN isbreed ib ON d.dog_id = ib.dog_id
            LEFT JOIN breed b ON ib.breed_name = b.breed_name
            WHERE d.dog_id = ?
            GROUP BY d.dog_id, d.dog_name, d.sex, d.altered, d.age, d.description, 
                     d.surrender_date, d.surrendered_by_animal_control
        ", [$dogId]);
        
        if (!$dog) {
            return redirect()->route('adoptions.select_dog', ['email' => $email, 'date' => $date])
                ->withErrors(['error' => 'Dog not found']);
        }
        
        $totalExpenses = DB::selectOne("
            SELECT COALESCE(SUM(cost), 0) as total 
            FROM expense 
            WHERE dog_id = ?
        ", [$dogId])->total;
        
        $adoptionFee = $this->calculateAdoptionFee($dog, $totalExpenses);
        
        return view('adoptions.confirm', [
            'applicant' => $applicant,
            'dog' => $dog,
            'totalExpenses' => $totalExpenses,
            'adoptionFee' => $adoptionFee
        ]);
    }
    
    public function processAdoption(Request $request)
    {
        $validated = $request->validate([
            'applicant_email' => 'required|email',
            'application_date' => 'required|date',
            'dog_id' => 'required|integer',
            'adoption_date' => 'required|date',
            'adoption_fee' => 'required|numeric'
        ]);
        
        try {
            DB::beginTransaction();
            
            DB::insert("
                INSERT INTO adoptedrelation (applicant_email, application_date, dog_id, adoption_date, fee)
                VALUES (?, ?, ?, ?, ?)
            ", [
                $validated['applicant_email'],
                $validated['application_date'],
                $validated['dog_id'],
                $validated['adoption_date'],
                $validated['adoption_fee']
            ]);
            
            DB::commit();
            
            return redirect()->route('dogdashboard')
                ->with('success', 'Dog has been successfully adopted!');
                
        } catch (\Exception $e) {
            DB::rollBack();
            return back()->withErrors(['error' => 'Failed to process adoption: ' . $e->getMessage()]);
        }
    }
    
    private function calculateAdoptionFee($dog, $totalExpenses)
    {
        $fee = 0;
        $isTerrier = false;
        $isSideways = false;
        
        if (strpos(strtolower($dog->breeds), 'terrier') !== false) {
            $isTerrier = true;
        }
        
        if (strtolower($dog->dog_name) === 'sideways') {
            $isSideways = true;
        }
        
        if ($dog->surrendered_by_animal_control) {
            $fee = $totalExpenses * 0.1;
        } else {
            $fee = $totalExpenses * 1.25;
        }
        
        if ($isTerrier && $isSideways) {
            $feeText = number_format($fee, 2) . " (waived)";
            return $feeText;
        }
        
        return $fee;
    }
}