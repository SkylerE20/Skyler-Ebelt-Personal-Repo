<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class ExpenseFormCont extends Controller
{
    public function expenseList(Request $request) {
        $dogId = (int) $request->route('dog_id');

        $dogDetail = DB::selectOne("SELECT dog.dog_id, dog.dog_name FROM dog WHERE dog_id = ?", [$dogId]);

        $categories = DB::select("SELECT category_name FROM category;");
       
        return view('ExpenseForm', compact('dogDetail','categories'));
    }

    public function addNewExpense(Request $request) {
        $dogId = (int) $request->route('dog_id');

        $validated = $request->validate([
            'newDate'  => 'required|date|before:now',
            'newVendor' =>  'required|string|max:249',
            'newCost' => 'required',
            'newCategory' => 'required'
        ]);

        $newDate = $validated['newDate'];

        $newVendor = $validated['newVendor'];

        $newCost = $validated['newCost'];

        $newCategory = $validated['newCategory'];
      
        DB::insert('INSERT INTO expense VALUES (?, ?, ?, ?, ?)'
        , [$dogId, $newDate, $newVendor, $newCost, $newCategory]);

        return redirect()->back()->with('success', 'Expense updated successfully');
    }
    
}
