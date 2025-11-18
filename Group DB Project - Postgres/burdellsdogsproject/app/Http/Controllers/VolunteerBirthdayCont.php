<?php

namespace App\Http\Controllers;

use Carbon\Carbon;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class VolunteerBirthdayCont extends Controller
{

    public function showVolunteerBirthday(Request $request) {

        $monthdd = $request->input('monthdd', Carbon::now()->month);

        $yeardd = $request->input('yeardd', 0);

        $volunteerBirthdayTable = DB::select(
            "
            SELECT
                first_name,
                last_name,
                email_address,
                CASE
                    WHEN (EXTRACT(YEAR FROM current_date) - ? - EXTRACT(YEAR FROM birth_date)) % 10 = 0 THEN TRUE
                    ELSE FALSE
                END AS milestone_birthday
            FROM Volunteer
            WHERE
            EXTRACT(MONTH FROM birth_date) = ?
            "
            , [$yeardd, $monthdd]
        );

        return view('VolunteerBirthday', compact('volunteerBirthdayTable', 'monthdd', 'yeardd'));
    }
}
