<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Illuminate\Validation\Rule;

class AdoptionApplicationController extends Controller
{
    

    public function create()
    {
        $availableDogs = DB::select("
            SELECT d.dog_id, d.dog_name, d.sex, d.age, d.description,
                  STRING_AGG(ib.breed_name, ', ') as breeds
            FROM dog d
            LEFT JOIN isbreed ib ON d.dog_id = ib.dog_id
            LEFT JOIN (
                SELECT dog_id FROM adoptedrelation 
                WHERE adoption_date <= CURRENT_DATE
            ) ar ON d.dog_id = ar.dog_id
            WHERE ar.dog_id IS NULL
            GROUP BY d.dog_id, d.dog_name, d.sex, d.age, d.description
            ORDER BY d.dog_name
        ");
        
        return view('applications.create', ['availableDogs' => $availableDogs]);
    }
    
    public function store(Request $request)
    {
        $validated = $request->validate([
            'dog_id' => [
                'required',
                'integer',
                Rule::exists('dog', 'dog_id')->where(function ($query) {
                    $query->whereNotExists(function ($subquery) {
                        $subquery->select(DB::raw(1))
                               ->from('adoptedrelation')
                               ->whereRaw('adoptedrelation.dog_id = dog.dog_id')
                               ->where('adoption_date', '<=', date('Y-m-d'));
                    });
                }),
            ],
            'first_name' => 'required|string|max:250',
            'last_name' => 'required|string|max:250',
            'applicant_email' => 'required|email|max:250',
            'applicant_phone' => 'required|string|max:20',
            'household_size' => 'required|integer|min:1',
            'state_abbrev' => 'required|string|size:2',
            'city' => 'required|string|max:250',
            'street' => 'required|string|max:250',
            'zip_code' => 'required|string|max:250'
        ], [
            'dog_id.required' => 'Please select a dog to adopt.',
            'dog_id.exists' => 'The selected dog is not available for adoption.'
        ]);
        
        DB::beginTransaction();
        
        try {
            $adopter = DB::selectOne("
                SELECT * FROM adopter WHERE applicant_email = ?
            ", [$validated['applicant_email']]);
            
            if (!$adopter) {
                DB::insert("
                    INSERT INTO adopter 
                    (applicant_email, first_name, last_name, applicant_phone, household_size, state_abbrev, city, street, zip_code)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ", [
                    $validated['applicant_email'],
                    $validated['first_name'],
                    $validated['last_name'],
                    $validated['applicant_phone'],
                    $validated['household_size'],
                    strtoupper($validated['state_abbrev']),
                    $validated['city'],
                    $validated['street'],
                    $validated['zip_code']
                ]);
            } else {
                DB::update("
                    UPDATE adopter
                    SET first_name = ?, last_name = ?, applicant_phone = ?, 
                        household_size = ?, state_abbrev = ?, city = ?, 
                        street = ?, zip_code = ?
                    WHERE applicant_email = ?
                ", [
                    $validated['first_name'],
                    $validated['last_name'],
                    $validated['applicant_phone'],
                    $validated['household_size'],
                    strtoupper($validated['state_abbrev']),
                    $validated['city'],
                    $validated['street'],
                    $validated['zip_code'],
                    $validated['applicant_email']
                ]);
            }
            
            $todayDate = date('Y-m-d');
            
            $existingApplication = DB::selectOne("
                SELECT * FROM application 
                WHERE applicant_email = ? AND application_date = ?
            ", [$validated['applicant_email'], $todayDate]);
            
            if (!$existingApplication) {
                DB::insert("
                    INSERT INTO application (applicant_email, application_date)
                    VALUES (?, ?)
                ", [$validated['applicant_email'], $todayDate]);
            }
            
            $dogAdopted = DB::selectOne("
                SELECT * FROM adoptedrelation
                WHERE dog_id = ? AND adoption_date <= ?
            ", [$validated['dog_id'], $todayDate]);
            
            if ($dogAdopted) {
                throw new \Exception('This dog has already been adopted.');
            }
            
            $existingRelation = DB::selectOne("
                SELECT * FROM adoptedrelation
                WHERE applicant_email = ? AND application_date = ? AND dog_id = ?
            ", [$validated['applicant_email'], $todayDate, $validated['dog_id']]);
            
            if (!$existingRelation) {
                $placeholderDate = date('Y-m-d', strtotime('+100 years'));
                
                DB::insert("
                    INSERT INTO adoptedrelation (applicant_email, application_date, dog_id, adoption_date, fee)
                    VALUES (?, ?, ?, ?, ?)
                ", [$validated['applicant_email'], $todayDate, $validated['dog_id'], $placeholderDate, 0.00]);
            }
            
            DB::commit();
            
            return redirect()->route('applications.success')
                ->with('email', $validated['applicant_email'])
                ->with('date', $todayDate)
                ->with('dog_id', $validated['dog_id']);
        } catch (\Exception $e) {
            DB::rollBack();
            
            return redirect()->back()
                ->withInput()
                ->withErrors(['error' => 'Application submission failed: ' . $e->getMessage()]);
        }
    }
    
    public function success()
    {
        $email = session('email');
        $date = session('date');
        $dogId = session('dog_id');
        
        if (!$email || !$date) {
            return redirect()->route('applications.create');
        }
        
        $dog = null;
        if ($dogId) {
            $dog = DB::selectOne("
                SELECT d.dog_id, d.dog_name, d.sex, d.age, d.description,
                      STRING_AGG(ib.breed_name, ', ') as breeds
                FROM dog d
                LEFT JOIN isbreed ib ON d.dog_id = ib.dog_id
                WHERE d.dog_id = ?
                GROUP BY d.dog_id, d.dog_name, d.sex, d.age, d.description
            ", [$dogId]);
        }
        
        return view('applications.success', [
            'email' => $email,
            'date' => $date,
            'dog' => $dog
        ]);
    }
    
    public function index(Request $request)
{
    $isExecutiveDirector = true;
    
    $searchLastName = $request->input('search_last_name');
    $searchStatus = $request->input('status', 'all');
    
    $baseQuery = "
        SELECT 
            a.applicant_email, 
            a.application_date,
            ad.first_name, 
            ad.last_name, 
            ad.applicant_phone, 
            ad.household_size,
            CASE 
                WHEN aa.applicant_email IS NOT NULL THEN 'Approved'
                WHEN ra.applicant_email IS NOT NULL THEN 'Rejected'
                ELSE 'Pending'
            END as status,
            aa.accept_date,
            ra.reject_date,
            ar.dog_id,
            d.dog_name,
            d.sex,
            d.age,
            d.description,
            CASE 
                WHEN ar.adoption_date > '2100-01-01' THEN NULL
                ELSE ar.adoption_date
            END as actual_adoption_date,
            ar.fee
        FROM application a
        JOIN adopter ad ON a.applicant_email = ad.applicant_email
        LEFT JOIN approvedapplication aa ON a.applicant_email = aa.applicant_email 
            AND a.application_date = aa.application_date
        LEFT JOIN rejectedapplication ra ON a.applicant_email = ra.applicant_email 
            AND a.application_date = ra.application_date
        LEFT JOIN adoptedrelation ar ON a.applicant_email = ar.applicant_email 
            AND a.application_date = ar.application_date
        LEFT JOIN dog d ON ar.dog_id = d.dog_id
    ";
    
    $whereClause = " WHERE aa.applicant_email IS NULL AND ra.applicant_email IS NULL";
    $statusClause = "'Pending' as status";
    
    if ($searchStatus === 'approved') {
        $whereClause = " WHERE aa.applicant_email IS NOT NULL";
        $statusClause = "'Approved' as status";
    } elseif ($searchStatus === 'rejected') {
        $whereClause = " WHERE ra.applicant_email IS NOT NULL";
        $statusClause = "'Rejected' as status";
    } elseif ($searchStatus === 'all') {
        $whereClause = " WHERE 1=1";
        $statusClause = "CASE 
            WHEN aa.applicant_email IS NOT NULL THEN 'Approved'
            WHEN ra.applicant_email IS NOT NULL THEN 'Rejected'
            ELSE 'Pending'
        END as status";
    }
    
    $params = [];
    
    if (!empty($searchLastName)) {
        $whereClause .= " AND ad.last_name ILIKE ?";
        $params[] = '%' . $searchLastName . '%';
    }
    
    $orderClause = " ORDER BY a.application_date DESC";
    
    $query = str_replace("'Pending' as status", $statusClause, $baseQuery) . $whereClause . $orderClause;
    
    $applications = DB::select($query, $params);
    
    return view('applications.index', [
        'applications' => $applications,
        'isExecutiveDirector' => $isExecutiveDirector,
        'searchLastName' => $searchLastName,
        'searchStatus' => $searchStatus
    ]);
}
   
public function review($email, $date)
{
    $isExecutiveDirector = true;
    
    $application = DB::selectOne("
        SELECT a.applicant_email, a.application_date, 
               ad.first_name, ad.last_name, ad.applicant_phone, 
               ad.household_size, ad.state_abbrev, ad.city, ad.street, ad.zip_code,
               CASE 
                   WHEN aa.applicant_email IS NOT NULL THEN 'Approved'
                   WHEN ra.applicant_email IS NOT NULL THEN 'Rejected'
                   ELSE 'Pending'
               END as status,
               aa.accept_date,
               ra.reject_date
        FROM application a
        JOIN adopter ad ON a.applicant_email = ad.applicant_email
        LEFT JOIN approvedapplication aa ON a.applicant_email = aa.applicant_email AND a.application_date = aa.application_date
        LEFT JOIN rejectedapplication ra ON a.applicant_email = ra.applicant_email AND a.application_date = ra.application_date
        WHERE a.applicant_email = ? AND a.application_date = ?
    ", [$email, $date]);
    
    if (!$application) {
        return redirect()->route('applications.index')
            ->withErrors(['error' => 'Application not found']);
    }
    
    $relations = DB::select("
        SELECT * FROM adoptedrelation 
        WHERE applicant_email = ? AND application_date = ?
    ", [$email, $date]);
    
    if (empty($relations)) {
        return view('applications.review', [
            'application' => $application,
            'relatedDogs' => [],
            'isExecutiveDirector' => $isExecutiveDirector,
            'error' => 'No dog association found for this application.'
        ]);
    }
    
    $dogIds = array_map(function($rel) { 
        return $rel->dog_id; 
    }, $relations);
    
    $placeholders = implode(',', array_fill(0, count($dogIds), '?'));
    
    $dogs = DB::select("
        SELECT d.*,
              STRING_AGG(ib.breed_name, ', ') as breeds
        FROM dog d
        LEFT JOIN isbreed ib ON d.dog_id = ib.dog_id
        WHERE d.dog_id IN ($placeholders)
        GROUP BY d.dog_id, d.dog_name, d.sex, d.age, d.description
    ", $dogIds);
    
    $relatedDogs = [];
    foreach ($relations as $relation) {
        foreach ($dogs as $dog) {
            if ($relation->dog_id == $dog->dog_id) {
                $combined = (object) array_merge(
                    (array) $relation,
                    (array) $dog,
                    [
                        'actual_adoption_date' => $relation->adoption_date > '2100-01-01' ? null : $relation->adoption_date
                    ]
                );
                $relatedDogs[] = $combined;
                break;
            }
        }
    }
    //this is a test!
    return view('applications.review', [
        'application' => $application,
        'relatedDogs' => $relatedDogs,
        'isExecutiveDirector' => $isExecutiveDirector
    ]);
}
    public function approve($email, $date)
    {
        $isExecutiveDirector = true;
        
        $application = DB::selectOne("
            SELECT a.*, 
                   CASE 
                       WHEN aa.applicant_email IS NOT NULL THEN 'Approved'
                       WHEN ra.applicant_email IS NOT NULL THEN 'Rejected'
                       ELSE 'Pending'
                   END as status
            FROM application a
            LEFT JOIN approvedapplication aa ON a.applicant_email = aa.applicant_email AND a.application_date = aa.application_date
            LEFT JOIN rejectedapplication ra ON a.applicant_email = ra.applicant_email AND a.application_date = ra.application_date
            WHERE a.applicant_email = ? AND a.application_date = ?
        ", [$email, $date]);
        
        if (!$application) {
            return redirect()->route('applications.index')
                ->withErrors(['error' => 'Application not found']);
        }
        
        if ($application->status !== 'Pending') {
            return redirect()->route('applications.review', ['email' => $email, 'date' => $date])
                ->withErrors(['error' => 'This application has already been ' . $application->status]);
        }
    
        $todayDate = date('Y-m-d');
        
        DB::beginTransaction();
        
        try {
            DB::insert("
                INSERT INTO approvedapplication (applicant_email, application_date, accept_date)
                VALUES (?, ?, ?)
            ", [$email, $date, $todayDate]);
            
            DB::update("
                UPDATE adoptedrelation 
                SET adoption_date = ?, fee = 150.00
                WHERE applicant_email = ? AND application_date = ?
            ", [$todayDate, $email, $date]);
            
            DB::commit();
            
            return redirect()->route('applications.index')
                ->with('success', 'Application has been approved successfully');
        } catch (\Exception $e) {
            DB::rollBack();
            
            return redirect()->back()
                ->withErrors(['error' => 'Approval failed: ' . $e->getMessage()]);
        }
    }
    
    public function reject($email, $date)
    {
        $isExecutiveDirector = true;
        
        $application = DB::selectOne("
            SELECT a.*, 
                   CASE 
                       WHEN aa.applicant_email IS NOT NULL THEN 'Approved'
                       WHEN ra.applicant_email IS NOT NULL THEN 'Rejected'
                       ELSE 'Pending'
                   END as status
            FROM application a
            LEFT JOIN approvedapplication aa ON a.applicant_email = aa.applicant_email AND a.application_date = aa.application_date
            LEFT JOIN rejectedapplication ra ON a.applicant_email = ra.applicant_email AND a.application_date = ra.application_date
            WHERE a.applicant_email = ? AND a.application_date = ?
        ", [$email, $date]);
    
        if (!$application) {
            return redirect()->route('applications.index')
                ->withErrors(['error' => 'Application not found']);
        }
        
        if ($application->status !== 'Pending') {
            return redirect()->route('applications.review', ['email' => $email, 'date' => $date])
                ->withErrors(['error' => 'This application has already been ' . $application->status]);
        }
        
        $todayDate = date('Y-m-d');
        
        DB::beginTransaction();
        
        try {
            DB::insert("
                INSERT INTO rejectedapplication (applicant_email, application_date, reject_date)
                VALUES (?, ?, ?)
            ", [$email, $date, $todayDate]);
            
            DB::delete("
                DELETE FROM adoptedrelation
                WHERE applicant_email = ? AND application_date = ?
            ", [$email, $date]);
            
            DB::commit();
            
            return redirect()->route('applications.index')
                ->with('success', 'Application has been rejected successfully');
        } catch (\Exception $e) {
            DB::rollBack();
            
            return redirect()->back()
                ->withErrors(['error' => 'Rejection failed: ' . $e->getMessage()]);
        }
    }
}