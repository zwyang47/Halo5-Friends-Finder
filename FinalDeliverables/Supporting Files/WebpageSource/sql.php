<?php
include 'config.php';

function connectSql() {
  $mysqli = new mysqli('localhost', 'zhiweiyang', '650230', 'xboxhalo5');
  if ($mysqli->connect_errno) {
    exitWithError(sprintf("Connection Failed: %s\n", $mysqli->connect_error));
  }
  else {
    $GLOBALS['mysqli'] = $mysqli;
  }
  return $mysqli;
}

function getConnectedSql() {
  if (!isset($GLOBALS['mysqli']))
    connectSql();
  $mysqli = $GLOBALS['mysqli'];
  return $mysqli;
}

function sqlError($mysqli, $stmt) {
  if(!$stmt) {
    return $mysqli->errno;
  }
  if($stmt && $stmt->errno != 0) {
    return $stmt->errno;
  }
  return 0;
}

function exitIfStatementFailed($mysqli, $stmt) {
  if(!$stmt) {
    $GLOBAL['error'] = sprintf("Statement preparation failed: %s", $mysqli->error);
  }
  if($stmt && $stmt->errno != 0) {
    $GLOBAL['error'] = sprintf("Statement execution failed: %s", $stmt->error);
  }
  exitIfError();
}

function sqlTime($time=null) {
  if (is_null($time))
    $time = time();
  $format = 'Y-m-d H:i:s';
  return date($format, $time);
}

// Return the unclosed mysqli_stmt or null
function _sqlExecuteStart($stmtStr, $bindParamFormat='', $bindParamArray=null) {
  $mysqli = getConnectedSql();
  $stmt = $mysqli->prepare($stmtStr);
  if (!$stmt)
    return null;
  // Call $stmt->bind_param 
  if ($bindParamFormat !== '' && is_array($bindParamArray)) {
    call_user_func_array(array($stmt, 'bind_param'), 
      array_merge((array)$bindParamFormat, $bindParamArray));
  }
  $stmt->execute();
  return $stmt;
}

// Return the error code or 0 if succeeded
function sqlExecute($stmtStr, $bindParamFormat='', $bindParamArray=null) {
  $mysqli = getConnectedSql();
  $stmt = _sqlExecuteStart($stmtStr, $bindParamFormat, $bindParamArray);
  $errno = sqlError($mysqli, $stmt);
  $stmt->close();
  return $errno;
}

// Return the query object or null if failed
function sqlExecuteGetFirst($stmtStr, $bindParamFormat='', $bindParamArray=null) {
  $mysqli = getConnectedSql();
  $stmt = _sqlExecuteStart($stmtStr, $bindParamFormat, $bindParamArray);
  $errno = sqlError($mysqli, $stmt);
  if ($errno)
    return null;
  // $row may be null if no such data exists
  $row = $stmt->get_result()->fetch_assoc();
  $stmt->close();
  return $row;
}

// Return null if error
// Return the number of rows
function sqlExecuteForEach($callback, $stmtStr, $bindParamFormat='', $bindParamArray=null) {
  $mysqli = getConnectedSql();
  $stmt = _sqlExecuteStart($stmtStr, $bindParamFormat, $bindParamArray);
  $errno = sqlError($mysqli, $stmt);
  $num = 0;
  if ($errno)
    return 0;
  try {
    $result = $stmt->get_result();
    while($row = $result->fetch_assoc()){
      $num++;
      $callback($row);
    }
  } finally {
    $stmt->close();
  }
  return $num;
}
?>
