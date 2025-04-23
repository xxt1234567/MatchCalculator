<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
ini_set('max_execution_time', 60);
class CalculationController extends Controller
{
    public function calculate(Request $request)
    {
        $pythonScriptPath = escapeshellcmd(realpath(__DIR__ . '/matchcalculator.py'));
        $scoreboard = $request->input('scoreboard');
        $matchleft = $request->input('matchleft');
        $matchleftcnt = $request->input('matchleftcnt');
        $teamcnt = $request->input('teamcnt');
        $bo = $request->input('bo');
        $double = $request->input('double');
        $wscore = $request->input('wscore');
        $lscore = $request->input('lscore');
        $dscore = $request->input('dscore');
        $showtop = $request->input('showtop');
        $showbot = $request->input('showbot');
        $toprank = $request->input('toprank');
        $botrank = $request->input('botrank');
        $sadd = $request->input('sadd');
        $srank = $request->input('srank');
        $snext = $request->input('snext');
        $steam = $request->input('steam');
        $steamr1 = $request->input('steamr1');
        $steamr2 = $request->input('steamr2');
        $nteam1 = $request->input('nteam1');
        $nteam2 = $request->input('nteam2');
        $mostml = $request->input('mostml');

        $jscoreboard = escapeshellarg(json_encode($scoreboard));
        $jmatchleft = escapeshellarg(json_encode($matchleft));
        
        $output = shell_exec("python $pythonScriptPath $jscoreboard $jmatchleft $matchleftcnt $teamcnt $bo $double $wscore $lscore $dscore $showtop $showbot $toprank $botrank $sadd $srank $snext $steam $steamr1 $steamr2 $nteam1 $nteam2 $mostml 2>&1");
        if (strpos($output, '"status": "error"') !== false) {
            $errorData = json_decode($output, true);
            return response()->json([
                'status' => 'error',
                'message' => $errorData['message'] ?? 'Python脚本执行错误'
            ]);
        } else {
            return response()->json([
                'status' => 'success',
                'res' => $output
            ]);
        }
    }
}
