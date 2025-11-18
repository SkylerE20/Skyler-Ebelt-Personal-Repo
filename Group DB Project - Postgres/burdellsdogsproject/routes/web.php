<?php

use App\Http\Controllers\LoginCont;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\DogDetailsCont;
use App\Http\Controllers\DogDashboardCont;
use App\Http\Controllers\ExpenseAnalysisCont;
use App\Http\Controllers\MonthlyAdoptionCont;
use App\Http\Controllers\VolunteerLookupCont;
use App\Http\Controllers\VolunteerBirthdayCont;
use App\Http\Controllers\AdoptionApplicationController;
use App\Http\Controllers\AnimalControlReportController;
use App\Http\Controllers\NewDogCont;
use App\Http\Controllers\ExpenseFormCont;

Route::get('/', function () {
    return view('login');
});

Route::post('/login', [LoginCont::class, 'loginf']);

Route::middleware(['volval'])->group(function () {
    Route::post('/dogdashboard', [DogDashboardCont::class, 'showDogDashboard']);
    Route::get('/dogdashboard', [DogDashboardCont::class, 'showDogDashboard']);
    Route::get('/dogdetails', [DogDetailsCont::class, 'index']);
    Route::get('/dogdetails/{dog_id}', [DogDetailsCont::class, 'showDogDetails']);
    Route::post('/dogdetails/{dog_id}', [DogDetailsCont::class, 'updateDogDetail']);
    Route::post('/addNewDog', [NewDogCont::class, 'addNewDog']);
    Route::get('/addNewDog', [NewDogCont::class, 'volunteerEmails']);
    Route::get('/expenseForm/{dog_id}', [ExpenseFormCont::class, 'expenseList']);
    Route::post('/expenseForm/{dog_id}', [ExpenseFormCont::class, 'addNewExpense']);
});

Route::middleware(['execval'])->group(function () {
    Route::get('/AdoptionAppDash', [AdoptionDashboardController::class, 'showAdoptionDashboard']);
    Route::get('/reports/animal-control', [AnimalControlReportController::class, 'index']);
    Route::get('/MonthlyAdoption', [MonthlyAdoptionCont::class, 'showMonthlyAdoption']);
    Route::get('/ExpenseAnalysis', [ExpenseAnalysisCont::class, 'showExpenseAnalysis']);
    Route::get('/VolunteerLookup', [VolunteerLookupCont::class, 'showVolunteerLookup']);
    Route::post('/VolunteerLookup', [VolunteerLookupCont::class, 'volunteerLookupf']);
    Route::get('/VolunteerBirthday', [VolunteerBirthdayCont::class, 'showVolunteerBirthday']);
    Route::post('/VolunteerBirthday', [VolunteerBirthdayCont::class, 'showVolunteerBirthday']);
});

Route::get('/apply', [AdoptionApplicationController::class, 'create'])->name('applications.create');

Route::post('/apply', [AdoptionApplicationController::class, 'store'])->name('applications.store');

Route::get('/apply/success', [AdoptionApplicationController::class, 'success'])->name('applications.success');

Route::get('/applications', [AdoptionApplicationController::class, 'index'])->name('applications.index');

Route::get('/applications/{email}/{date}', [AdoptionApplicationController::class, 'review'])->name('applications.review');

Route::post('/applications/{email}/{date}/approve', [AdoptionApplicationController::class, 'approve'])->name('applications.approve');

Route::post('/applications/{email}/{date}/reject', [AdoptionApplicationController::class, 'reject'])->name('applications.reject');

Route::get('/reports/animal-control', [AnimalControlReportController::class, 'index'])
    ->name('animal-control-report');

Route::get('/reports/drill-down/surrendered/{startDate}/{endDate}', [AnimalControlReportController::class, 'surrenderedDrillDown'])
    ->name('drill-down-surrendered');

Route::get('/reports/drill-down/60plus/{startDate}/{endDate}', [AnimalControlReportController::class, 'sixtyPlusDrillDown'])
    ->name('drill-down-60plus');

Route::get('/reports/drill-down/expenses/{startDate}/{endDate}', [AnimalControlReportController::class, 'expensesDrillDown'])
    ->name('drill-down-expenses');

Route::get('/applications/create', [App\Http\Controllers\AdoptionApplicationController::class, 'create'])
    ->name('applications.create');
    
Route::post('/applications', [App\Http\Controllers\AdoptionApplicationController::class, 'store'])
    ->name('applications.store');
    
Route::get('/applications/success', [App\Http\Controllers\AdoptionApplicationController::class, 'success'])
    ->name('applications.success');
    
Route::get('/applications', [App\Http\Controllers\AdoptionApplicationController::class, 'index'])
    ->name('applications.index');
    
Route::get('/applications/{email}/{date}', [App\Http\Controllers\AdoptionApplicationController::class, 'review'])
    ->name('applications.review');
    
Route::post('/applications/{email}/{date}/approve', [App\Http\Controllers\AdoptionApplicationController::class, 'approve'])
    ->name('applications.approve');
    
Route::post('/applications/{email}/{date}/reject', [App\Http\Controllers\AdoptionApplicationController::class, 'reject'])
    ->name('applications.reject');

Route::get('/adoptions', [App\Http\Controllers\AdoptionController::class, 'index'])
    ->name('adoptions.index');

Route::post('/adoptions/search', [App\Http\Controllers\AdoptionController::class, 'searchApplications'])
    ->name('adoptions.search');
    
Route::get('/adoptions/select-dog/{email}/{date}', [App\Http\Controllers\AdoptionController::class, 'selectDog'])
    ->name('adoptions.select_dog');
    
Route::get('/adoptions/confirm/{email}/{date}/{dogId}', [App\Http\Controllers\AdoptionController::class, 'confirmAdoption'])
    ->name('adoptions.confirm');
    
Route::post('/adoptions/process', [App\Http\Controllers\AdoptionController::class, 'processAdoption'])
    ->name('adoptions.process');
