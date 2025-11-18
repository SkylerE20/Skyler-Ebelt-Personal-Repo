<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class MonthlyAdoptionCont extends Controller
{
    public function showMonthlyAdoption()
    {
        $monthlyAdoptionTable = DB::select(
            "
            -- dogid | suranimalcont? | breedname as one, aggregate breeds
            WITH DogBreedConcat AS (
                SELECT
                    d.dog_id,
                    d.surrendered_by_animal_control,
                    STRING_AGG(ib.breed_name, '/' ORDER BY ib.breed_name) AS breed_name
                FROM Dog d
                JOIN IsBreed ib ON d.dog_id = ib.dog_id
                GROUP BY d.dog_id, d.surrendered_by_animal_control
            ),

            -- dogid | total expenses, aggregate expenses
            DogExpenseCost AS (
                SELECT
                    dog_id,
                    COALESCE(SUM(cost), 0) AS cost
                FROM Expense
                GROUP BY dog_id
            ),
            
            -- month | breed | surrender count, aggregate surrender count
            Surrendered AS (
                SELECT
                    DATE_TRUNC('month', d.surrender_date) AS monthcol,
                    dbc.breed_name,
                    COUNT(DISTINCT d.dog_id) AS surrendered_count
                FROM Dog d
                JOIN DogBreedConcat dbc ON d.dog_id = dbc.dog_id
                WHERE d.surrender_date >= DATE_TRUNC('month', CURRENT_DATE) - INTERVAL '12 months'
                AND d.surrender_date < DATE_TRUNC('month', CURRENT_DATE)
                GROUP BY monthcol, breed_name
            ),

            -- calculate fields for adopted dogs
            Adopted AS (
                SELECT
                    DATE_TRUNC('month', a.adoption_date) AS monthcol,
                    dbc.breed_name,
                    COUNT(DISTINCT a.dog_id) AS adopted_count,
                    SUM(dec.cost) AS total_expenses,
                    SUM(
                        CASE
                            WHEN dbc.surrendered_by_animal_control = TRUE THEN dec.cost * 0.1
                            ELSE dec.cost * 1.25
                        END
                    ) AS total_fees,
                    SUM(
                        CASE
                            WHEN dbc.surrendered_by_animal_control = TRUE THEN 0
                            ELSE dec.cost
                        END
                    ) AS total_expenses_no_ac
                FROM AdoptedRelation a
                JOIN DogBreedConcat dbc ON a.dog_id = dbc.dog_id
                LEFT JOIN DogExpenseCost dec ON a.dog_id = dec.dog_id
                WHERE a.adoption_date >= DATE_TRUNC('month', CURRENT_DATE) - INTERVAL '12 months'
                AND a.adoption_date < DATE_TRUNC('month', CURRENT_DATE)
                GROUP BY monthcol, dbc.breed_name
            )
            
            -- coalesce surrendered and adopted
            SELECT
                TO_CHAR(COALESCE(s.monthcol, a.monthcol), 'YYYY-MM') AS monthcol,
                COALESCE(s.breed_name, a.breed_name) AS breed,
                COALESCE(a.adopted_count, 0) AS adopted_count,
                COALESCE(s.surrendered_count, 0) AS surrendered_count,
                COALESCE(a.total_expenses, 0) AS total_expenses,
                COALESCE(a.total_fees, 0) AS total_fees,
                COALESCE(a.total_fees, 0) - COALESCE(a.total_expenses_no_ac, 0) AS net_profit
            FROM Surrendered s
            FULL OUTER JOIN Adopted a ON s.monthcol = a.monthcol AND s.breed_name = a.breed_name
            ORDER BY monthcol ASC, breed ASC
        ");

        return view('MonthlyAdoption', ['monthlyAdoptionTable' => $monthlyAdoptionTable]);
    }
}
