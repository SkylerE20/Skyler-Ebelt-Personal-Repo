<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class AnimalControlReportController extends Controller
{
    // Display the Animal Control Report with monthly data
    public function index()
    {
        $months = [];
        
        for ($i = 0; $i < 7; $i++) {
            $endDate = date('Y-m-d', strtotime("last day of -$i month"));
            $startDate = date('Y-m-d', strtotime("first day of -$i month"));
            $monthLabel = date('F Y', strtotime($startDate));
            
            $acSurrendered = DB::selectOne("
                SELECT COUNT(*) as count 
                FROM dog 
                WHERE surrendered_by_animal_control = true 
                AND surrender_date BETWEEN ? AND ?
            ", [$startDate, $endDate])->count;
            
            $dogsAdopted60Plus = DB::selectOne("
                SELECT COUNT(*) as count 
                FROM adoptedrelation ar
                JOIN dog d ON ar.dog_id = d.dog_id
                WHERE ar.adoption_date BETWEEN ? AND ?
                AND (ar.adoption_date - d.surrender_date) >= 60
            ", [$startDate, $endDate])->count;
            
            $totalExpenses = DB::selectOne("
                SELECT COALESCE(SUM(cost), 0) as total 
                FROM expense 
                WHERE expense_date BETWEEN ? AND ?
            ", [$startDate, $endDate])->total;
            
            $months[] = [
                'month_label' => $monthLabel,
                'start_date' => $startDate,
                'end_date' => $endDate,
                'ac_surrendered' => $acSurrendered,
                '60plus' => $dogsAdopted60Plus,
                'total_expenses' => $totalExpenses
            ];
        }
        
        return view('animal-control', ['months' => $months]);
    }
    
    // Display drill-down details for surrendered animals in a specific period
    public function surrenderedDrillDown($startDate, $endDate)
    {
        $month = date('F Y', strtotime($startDate));
        
        $dogs = DB::select("
            SELECT d.dog_id, d.sex, d.altered, d.surrender_date, 
                   m.microchip_id,
                   STRING_AGG(b.breed_name, '/') as breed
            FROM dog d
            LEFT JOIN microchip m ON d.dog_id = m.dog_id
            LEFT JOIN isbreed ib ON d.dog_id = ib.dog_id
            LEFT JOIN breed b ON ib.breed_name = b.breed_name
            WHERE d.surrendered_by_animal_control = true 
            AND d.surrender_date BETWEEN ? AND ?
            GROUP BY d.dog_id, d.sex, d.altered, d.surrender_date, m.microchip_id
            ORDER BY d.surrender_date DESC
        ", [$startDate, $endDate]);
        
        return view('drill-down-surrendered', [
            'dogs' => $dogs,
            'month' => $month
        ]);
    }

    // Display drill-down details for 60+ day dogs adopted in a specific period
    public function sixtyPlusDrillDown($startDate, $endDate)
    {
        $month = date('F Y', strtotime($startDate));
        
        $dogs = DB::select("
            SELECT d.dog_id, d.sex, d.surrender_date, m.microchip_id,
                   ar.adoption_date, 
                   (ar.adoption_date - d.surrender_date) as days_in_rescue,
                   STRING_AGG(b.breed_name, '/') as breed
            FROM adoptedrelation ar
            JOIN dog d ON ar.dog_id = d.dog_id
            LEFT JOIN microchip m ON d.dog_id = m.dog_id
            LEFT JOIN isbreed ib ON d.dog_id = ib.dog_id
            LEFT JOIN breed b ON ib.breed_name = b.breed_name
            WHERE ar.adoption_date BETWEEN ? AND ?
            AND (ar.adoption_date - d.surrender_date) >= 60
            GROUP BY d.dog_id, d.sex, d.surrender_date, m.microchip_id, ar.adoption_date
            ORDER BY days_in_rescue DESC
        ", [$startDate, $endDate]);
        
        return view('drill-down-60plus', [
            'dogs' => $dogs,
            'month' => $month
        ]);
    }
    
    // Display drill-down details for expenses in a specific period
    public function expensesDrillDown($startDate, $endDate)
    {
        $month = date('F Y', strtotime($startDate));
        
        $dogs = DB::select("
            SELECT d.dog_id, d.sex, d.surrender_date, 
                   d.surrendered_by_animal_control as from_animal_control,
                   m.microchip_id,
                   STRING_AGG(DISTINCT b.breed_name, '/') as breed,
                   SUM(e.cost) as total_expenses
            FROM expense e
            JOIN dog d ON e.dog_id = d.dog_id
            LEFT JOIN microchip m ON d.dog_id = m.dog_id
            LEFT JOIN isbreed ib ON d.dog_id = ib.dog_id
            LEFT JOIN breed b ON ib.breed_name = b.breed_name
            WHERE e.expense_date BETWEEN ? AND ?
            GROUP BY d.dog_id, d.sex, d.surrender_date, d.surrendered_by_animal_control, m.microchip_id
            ORDER BY total_expenses DESC
        ", [$startDate, $endDate]);

        $total = array_reduce($dogs, function($carry, $dog) {
            return $carry + $dog->total_expenses;
        }, 0);
        
        return view('drill-down-expenses', [
            'dogs' => $dogs,
            'month' => $month,
            'total' => $total
        ]);
    }
}