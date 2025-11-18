<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class LoginCont extends Controller
{
    public function loginf(Request $request) {
        $incomingFields = $request->validate([
            'lemail' => 'required',
            'lpassword' => 'required'
        ]);


        // email check
        $vemail = DB::selectOne(
            '
            SELECT EXISTS (
                SELECT 1 FROM volunteer WHERE email_address = ?
            ) AS yes_exists
            '
        , [$incomingFields['lemail']]);

        if (!$vemail->yes_exists) {
            return back()->withErrors([
                'lemail' => 'User not found'
            ]);
        }

        // email and password check
        $volunteer = DB::selectOne(
            '
            SELECT EXISTS (
                SELECT 1
                FROM Volunteer
                WHERE email_address = ? AND volunteer_password = ?
            ) AS yes_exists
            '
        , [$incomingFields['lemail'], $incomingFields['lpassword']]);

        if (!$volunteer->yes_exists) {
            return back()->withErrors([
                'lpassword' => 'Incorrect password'
            ]);
        } else {
            // handle exec session attribute
            $exec = DB::selectOne(
                '
                SELECT EXISTS (
                    SELECT 1 FROM executivedirector WHERE email_address = ?
                ) AS yes_exists
                '
            , [$incomingFields['lemail']]);

            if ($exec->yes_exists) {
                session()->put('isExec', true);
            } else {
                session()->put('isExec', false);
            }
        }

        session()->put('email_address', $incomingFields['lemail']);

        return redirect('/dogdashboard');
    }
    
}
