<?php

namespace App\Http\Controllers;

use Illuminate\Support\Facades\DB;

class ExpenseAnalysisCont extends Controller
{
    public function showExpenseAnalysis()
    {
        $expenseAnalysisTable = DB::select("
            SELECT
                expense.expense_vendor AS vendor,
                SUM(expense.cost) AS total_expense
            FROM expense
            GROUP BY expense.expense_vendor
            ORDER BY total_expense DESC
    ");


        return view('ExpenseAnalysis', compact('expenseAnalysisTable'));
    }
}

