<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class VolunteerLookupCont extends Controller
{
    public function showVolunteerLookup() {
        return view('VolunteerLookup');
    }

    public function volunteerLookupf(Request $request) {

        $incomingFields = $request->validate([
            'searchInput' => 'required',
        ]);

        $search = '%' . $incomingFields['searchInput'] . '%';
        
        $volunteerLookup = DB::select(
            "
            SELECT 
                first_name,
                last_name, 
                email_address, 
                phone_number
            FROM volunteer
            WHERE first_name LIKE ? or last_name LIKE ?
            ORDER BY last_name, first_name
            "
            , [$search, $search]
        );
        
        return view('VolunteerLookup', compact('volunteerLookup'));
    }
}
