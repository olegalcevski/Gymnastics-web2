<?php
declare(strict_types=1);
if (session_status() !== PHP_SESSION_ACTIVE) { session_start(); }
header('Content-Type: application/json; charset=utf-8');
$configPath = __DIR__ . '/../config/config.php';
if (!file_exists($configPath)) { http_response_code(500); echo json_encode(['ok'=>false,'error'=>'Missing config/config.php']); exit; }
$config = require $configPath;
function out($data, int $code=200){ http_response_code($code); echo json_encode($data, JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES); exit; }
function db(){ global $config; static $pdo=null; if($pdo) return $pdo; $pdo = new PDO('mysql:host='.$config['db_host'].';dbname='.$config['db_name'].';charset=utf8mb4',$config['db_user'],$config['db_pass'],[PDO::ATTR_ERRMODE=>PDO::ERRMODE_EXCEPTION,PDO::ATTR_DEFAULT_FETCH_MODE=>PDO::FETCH_ASSOC]); return $pdo; }
function allowed_types(){ return ['settings','news','events','results','documents','people','gallery','clubs','partners','social','pages']; }
function require_admin(){ if(empty($_SESSION['fgsm_admin'])) out(['ok'=>false,'error'=>'Unauthorized'],401); }
function read_json_body(){ $raw=file_get_contents('php://input'); return $raw ? json_decode($raw,true) : []; }
function content_default($type){ return $type==='settings' ? [] : ['items'=>[]]; }
function get_payload($type){ if(!in_array($type, allowed_types(), true)) out(['ok'=>false,'error'=>'Invalid type'],400); $st=db()->prepare('SELECT payload FROM content_store WHERE type=?'); $st->execute([$type]); $row=$st->fetch(); if(!$row) return content_default($type); $data=json_decode($row['payload'],true); return $data ?: content_default($type); }
function save_payload($type,$payload){ if(!in_array($type, allowed_types(), true)) out(['ok'=>false,'error'=>'Invalid type'],400); $json=json_encode($payload, JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES|JSON_PRETTY_PRINT); $st=db()->prepare('INSERT INTO content_store(type,payload,updated_at) VALUES(?,?,NOW()) ON DUPLICATE KEY UPDATE payload=VALUES(payload), updated_at=NOW()'); $st->execute([$type,$json]); }
function item_key($item){ return $item['slug'] ?? $item['id'] ?? $item['title'] ?? $item['name'] ?? $item['date'] ?? ''; }
?>
