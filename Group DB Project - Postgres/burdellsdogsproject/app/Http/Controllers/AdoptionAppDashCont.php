<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class AdoptionAppDashCont extends Controller
{
    public function showAdoptionDashboard() {
        return view('AdoptionAppDash');
    }
}
