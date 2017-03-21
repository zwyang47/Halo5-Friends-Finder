<!DOCTYPE HTML> 
<html>
<head>
<title>Xbox One Halo 5 DB Project></title>
  <link href="assets/main.css" rel="stylesheet" type="text/css">
</head>
<body>
  <div class='body-wrapper'>
    <div class='row'>
      <div class='login'>
        <div id='title-logo' class='float-left'>
            </br>
          <a href='index.php'>
            <center><img src="assets/newXboxOne.jpg" alt="Xbox Logo" height="150" width="350"></center>
          </a>
        </div>
      </div>
    </div>

<?php
// define variables and set to empty values
include_once 'sql.php';

$gamertagErr = $searchErr = $xuidErr = $halo5Err = "";
$gamertag = $search = $xuid = $timePlayed = "";
$gamertagValid = $findFriends = $findGames = $findHalo5stats = false;
$friendsRec = $gamesRec = false;

if ($_SERVER["REQUEST_METHOD"] == "POST") {
   if (empty($_POST["gamertag"])) {
     $gamertagErr = "Gamertag is required";
   } else {
     $input = test_input($_POST["gamertag"]);
     $gamertag = strtolower($input);
     $row = sqlExecuteGetFirst("select xuid from PLAYERS where gamertag=?",
      's', array(&$gamertag));
      if (is_null($row))
        $xuidErr = "Gamertag not found";
      else
        $gamertagValid = true;
        $xuid = $row['xuid'];

   }
   
   if (empty($_POST["search"])) {
     $searchErr = "Search Option is required";
   } 
   else 
   {
     if ($gamertagValid)
     { 
        $search = test_input($_POST["search"]);
        switch($search)
        {
          case 'friends':
             $findFriends = true;
             break;
          case 'games':
             $findGames = true;
             break;
          case 'time':
             $row = sqlExecuteGetFirst("select sum(timeplayed) from GAMES_PLAYED where Playerxuid=?",
                's', array(&$xuid));
             $timePlayed = $row['sum(timeplayed)'];
             break;
          case 'halo5':
             $row = sqlExecuteGetFirst("select TotalGames from PLAYER_STATS where gamerxuid=?",
             's', array(&$xuid));
             if (is_null($row))
               $halo5Err = "No Halo 5 stats found";
             else
               $findHalo5stats = true;
               break;
          case 'friendsRec':
             $row = sqlExecuteGetFirst("select TotalGames from PLAYER_STATS where gamerxuid=?",
             's', array(&$xuid));
             if (is_null($row))
               $halo5Err = "No Halo 5 stats available to make recommendations";
             else
               $friendsRec = true;
             break;
          case 'gamesRec':
             $row = sqlExecuteGetFirst("select TotalGames from PLAYER_STATS where gamerxuid=?",
             's', array(&$xuid));
             if (is_null($row))
               $halo5Err = "No Halo 5 stats available to make recommendations";
             else
               $gamesRec = true;
             break;
          default:
             break;
         }
      } 
   }
}

function test_input($data) {
   $data = trim($data);
   $data = stripslashes($data);
   $data = htmlspecialchars($data);
   return $data;
}
?>

<h2><center>Xbox One & Halo 5 Friend Finder</center></h2>
<center><form method="post" action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]);?>"> 
   Gamertag: <input type="text" name="gamertag" value="<?php echo $gamertag?>">
   <span class="error">* <?php echo $gamertagErr;?></span>
   <br>
   <center>
   <table border='1' style='width:60%'>
   <tr><td><b>Individual Search Options</b></td><td><b>Recommendations &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp</b></td></tr>
   <tr><td><input type="radio" name="search" <?php if (isset($search) && $search=="friends") echo "checked";?>  value="friends">&nbsp Friends &nbsp</td>
   <td><input type="radio" name="search" <?php if (isset($search) && $search=="friendsRec") echo "checked";?>  value="friendsRec">&nbsp Friends &nbsp</td></tr>
   <tr><td><input type="radio" name="search" <?php if (isset($search) && $search=="games") echo "checked";?>  value="games">&nbsp Games &nbsp</td>
   <td><input type="radio" name="search" <?php if (isset($search) && $search=="gamesRec") echo "checked";?>  value="gamesRec">&nbsp Games &nbsp</td></tr>
   <tr><td><input type="radio" name="search" <?php if (isset($search) && $search=="time") echo "checked";?>  value="time">&nbsp Total Play Time &nbsp</td><td>&nbsp</td></tr>
   <tr><td><input type="radio" name="search" <?php if (isset($search) && $search=="halo5") echo "checked";?>  value="halo5">&nbsp Halo 5 Stats &nbsp</td><td>&nbsp</td></tr>
   </table></center>
   <span class="error">* <?php echo $searchErr;?></span>
   <br>
   <br>
   <input type="submit" name="submit" value="Submit"> 
</form></center>

<?php
echo "<h2><center>Results:</center></h2>";
echo "<center><b>$gamertag</b>";
echo "<br>";
if ($gamertagValid && !$findHalo5stats)
{
echo $halo5Err;
}
echo $xuidErr;
echo "<br>";
if ($search = 'time' && $timePlayed != '')
   echo "Total Time: $timePlayed Minutes";
else if($search = 'friends' && $findFriends)
{
   echo "<b>Friends:</b></br>";
   $count = sqlExecuteForEach(function($row){
        $fxuid = $row["fxuid"];
        $playerRow = sqlExecuteGetFirst("select gamertag from PLAYERS where xuid=?",
          's', array(&$fxuid));
        echo $playerRow['gamertag'];
        echo "</br>";
    },"select fxuid from FRIENDS_OF where pxuid=?", 'i', array(&$xuid));

    if ($count == 0)
        echo "No Friends Found</br>";
}
else if($search = 'halo5' && $findHalo5stats)
{
   echo "<b>Halo 5 Stats: </b></br>";
   echo "<center>";
   echo "<table border='1' style='width:95%'>";
   echo "<tr><td><b>Playlist</b></td><td><b>Season</b></td><td><b>Total Games</b></td>";
   echo "<td><b>Wins</b></td><td><b>Loses</b></td><td><b>Rank</b></td><td><b>Tier</b></td></tr>";
   $count = sqlExecuteForEach(function($row){
        $pid = $row["PlaylistID"];
        $playlistRow = sqlExecuteGetFirst("select pname from PLAYLISTS where pid=?", 's', array(&$pid));
        $pName = $playlistRow["pname"];
        $sid = $row["SeasonID"];
        $seasonRow = sqlExecuteGetFirst("select sname from SEASONS where sid=?", 's', array(&$sid));
        $sName = $seasonRow["sname"];
        $totalGames = $row["TotalGames"];
        $wins = $row["Wins"];
        $loses = $row["Loses"];
        $rankId = $row["Rank"];
        $rankRow = sqlExecuteGetFirst("select rankname from RANKS where rankid=?", 's', array(&$rankId));
        $rank = $rankRow["rankname"];
        $tier = $row["Tier"];
        echo "</td><td>$pName</td><td>$sName</td><td>$totalGames</td><td>$wins</td><td>$loses</td><td>$rank</td><td>$tier</td></tr>";
    },"select * from PLAYER_STATS where gamerxuid=? order by seasonid", 'i', array(&$xuid));
    echo "</table>";
    echo "</center>";

}
else if($search = 'games' && $findGames)
{
   echo "<b>Games:</b></br><center>";
   echo "<table border='1' style='width:80%'>";
   echo "<tr><td><b>Title</b></td><td><b>Time (Minutes)</b></td><td><b>Progress %</b></td></tr>";
   $count = sqlExecuteForEach(function($row){
        $gid = $row["gid"];
        $gTimePlayed = $row["timeplayed"];
        $gameProgress = $row["gameprogress"];
        $gameRow = sqlExecuteGetFirst("select gametitle from GAMES where gameid=?",
          's', array(&$gid));
        echo "<tr><td>";
        echo $gameRow['gametitle'];
        echo "</td><td>$gTimePlayed</td><td>$gameProgress</td></tr>";
    },"select gid, timeplayed, gameprogress from GAMES_PLAYED where playerxuid=?", 'i', array(&$xuid));
    echo "</table></center>";
    if ($count == 0)
        echo "No Games Found</br>";
}
else if($search = 'friendsRec' && $friendsRec)
{
   $myPids = array();
   $myRanks = array();
   $newFriends = array();
   echo "Players Playlists:";
   echo "<table border='1' style='width:40%'>";
   $count = sqlExecuteForEach(function($row){
        $pid = $row["PlaylistID"];
        $playlistRow = sqlExecuteGetFirst("select pname from PLAYLISTS where pid=?", 's', array(&$pid));
        $pName = $playlistRow["pname"];
        global $myPids;
        array_push($myPids, $pid);
        $rank = $row["Rank"];
        global $myRanks;
        array_push($myRanks, $rank);
    },"select * from PLAYER_STATS where gamerxuid=? and totalgames > 9 order by totalgames desc limit 3", 'i', array(&$xuid));
   if ($count == 0)
        echo "Not Enough Games Played</br>";
   else {
      $myCtr = 0;
      foreach($myPids as $mypid) {
         $playlistRow = sqlExecuteGetFirst("select pname from PLAYLISTS where pid=?", 's', array(&$mypid));
         echo "<tr><td>";
         echo $playlistRow["pname"];   
         echo "</td><td>";
         $rankRow = sqlExecuteGetFirst("select rankname from RANKS where rankid=?", 's', array(&$myRanks[$myCtr]));
         echo $rankRow["rankname"];
         echo "</td></tr>";
         $myCtr++;
      }
      echo "</table>";
      
      echo "<br><h2>Friend Recommendations:</h2>";
      $nonFriends = array();
      $count = sqlExecuteForEach(function($row){
        $nxuid = $row["xuid"];
        global $nonFriends;
        array_push($nonFriends, $nxuid);
      },"select xuid from PLAYERS where xuid!=? and xuid NOT IN (select fxuid from FRIENDS_OF where pxuid=?)", 'ss', array(&$xuid, &$xuid));

      foreach($nonFriends as $nonXUID) {
         unset($nonPids);
         $nonPids = array();
         $nonRanks = array();
         $count = sqlExecuteForEach(function($row){
            $pid = $row["PlaylistID"];
            $playlistRow = sqlExecuteGetFirst("select pname from PLAYLISTS where pid=?", 's', array(&$pid));
            $pName = $playlistRow["pname"];
            global $nonPids;
            array_push($nonPids, $pid);
            $rank = $row["Rank"];
            global $nonRanks;
            array_push($nonRanks, $rank);
        },"select PlaylistID, Rank from PLAYER_STATS where gamerxuid=? and totalgames > 9 order by totalgames desc limit 3", 'i', array(&$nonXUID));
        if($count > 0) {
           $ctr = 0;
           foreach($nonPids as $npid) {
              foreach($myPids as $mypid) {
                 if($mypid == $npid) {
                    $ctr++;
                 } 
              }
           }
           if($ctr > 1) {
              $newCtr = 0;
              $playerRow = sqlExecuteGetFirst("select gamertag from PLAYERS where xuid=?",'s', array(&$nonXUID));
              echo "<br>Gamertag: <b>";
              echo $playerRow['gamertag'];
              echo "</b><br>Playlists:";
              echo "<table border='1' style='width:40%'>";
              foreach($nonPids as $pid) {
                 $playlistRow = sqlExecuteGetFirst("select pname from PLAYLISTS where pid=?", 's', array(&$pid));
                 echo "<tr><td>";
                 echo $playlistRow["pname"];
                 echo "</td><td>";
                 $rankRow = sqlExecuteGetFirst("select rankname from RANKS where rankid=?", 's', array(&$nonRanks[$newCtr]));
                 echo $rankRow["rankname"];
                 echo "</td></tr>";
                 $newCtr++;
              }
              echo "</table>";
              echo "<br>";
           }
        }
        
      }
   }
}
else if($search = 'gamesRec' && $gamesRec)
{
   echo "<b>Player's Top 3 Games</b><br>";
   $myGids = array();
   $count = sqlExecuteForEach(function($row){
        $gid = $row["gid"];
        $gameRow = sqlExecuteGetFirst("select gametitle from GAMES where gameid=?",
          's', array(&$gid));
        $game = $gameRow['gametitle'];
        echo $game;
        global $myGids;
        array_push($myGids, $gid);
        echo "<br>";
    },"select gid from GAMES_PLAYED where playerxuid=? order by timeplayed desc limit 3", 'i', array(&$xuid));
    if ($count == 0)
        echo "No Games Found</br>";

   $myPids = array();
   $newFriends = array();
   $count = sqlExecuteForEach(function($row){
        $pid = $row["PlaylistID"];
        $playlistRow = sqlExecuteGetFirst("select pname from PLAYLISTS where pid=?", 's', array(&$pid));
        $pName = $playlistRow["pname"];
        global $myPids;
        array_push($myPids, $pid);
    },"select * from PLAYER_STATS where gamerxuid=? and totalgames > 9 order by totalgames desc limit 3", 'i', array(&$xuid));
   if ($count == 0)
        echo "Not Enough Games Played</br>";
   else {
      echo "<br><h2>Game Recommendations:</h2>";
      $nonFriends = array();
      $count = sqlExecuteForEach(function($row){
        $nxuid = $row["xuid"];
        global $nonFriends;
        array_push($nonFriends, $nxuid);
      },"select xuid from PLAYERS where xuid!=? and xuid NOT IN (select fxuid from FRIENDS_OF where pxuid=?)", 'ss', array(&$xuid, &$xuid));

      foreach($nonFriends as $nonXUID) {
         unset($nonPids);
         $nonPids = array();
         $count = sqlExecuteForEach(function($row){
            $pid = $row["PlaylistID"];
            $playlistRow = sqlExecuteGetFirst("select pname from PLAYLISTS where pid=?", 's', array(&$pid));
            $pName = $playlistRow["pname"];
            global $nonPids;
            array_push($nonPids, $pid);
        },"select PlaylistID, Rank from PLAYER_STATS where gamerxuid=? and totalgames > 9 order by totalgames desc limit 3", 'i', array(&$nonXUID));
        if($count > 0) {
           $ctr = 0;
           foreach($nonPids as $npid) {
              foreach($myPids as $mypid) {
                 if($mypid == $npid) {
                    $ctr++;
                 } 
              }
           }
           if($ctr > 1) {
              array_push($newFriends, $nonXUID);
           }
        }
      }
      foreach($newFriends as $fxuid) {
         $playerRow = sqlExecuteGetFirst("select gamertag from PLAYERS where xuid=?",'s', array(&$fxuid));
         echo "<br><b>";
         echo $playerRow['gamertag'];
         echo "</b><br>";
         $count = sqlExecuteForEach(function($row){
             global $myGids;
             $gid = $row["gid"];
             $found = false;
             foreach($myGids as $mygid) {
                 if($mygid == $gid) {
                   $found = true; 
                 } 
             } 
             if(!$found) {  
                $gameRow = sqlExecuteGetFirst("select gametitle from GAMES where gameid=?",'s', array(&$gid));
                echo $gameRow['gametitle'];
                echo "<br>";
             }
           },"select gid from GAMES_PLAYED where playerxuid=? order by timeplayed desc limit 3", 'i', array(&$fxuid));
      }
   }
}
echo " <br>";
echo "</center>"
?>

</body>
</html>
