<?php //print_r($_POST); die;
if(isset($_GET['nomor']) && $_GET['nomor'] != '' && isset($_GET['pesan']) && $_GET['pesan'] != '') {
$inp = file_get_contents('isimsg.json');
$tempArray = json_decode($inp);
$nomor = $_GET['nomor'];
$pesan = $_GET['pesan'];
if (substr($nomor, 0, 1) === '0') {
    $nomor = '62' . substr($nomor, 1);
}
$data = array('nomor' => $nomor, 'kode' => $pesan);
if(isset($_GET['img'])) {
    $expnama = explode('/',$_GET['img']);
    $nama = end($expnama);
    $target_file = __DIR__."/img/".time().'-'.$nama;
    copy($_GET['img'], $target_file);
    $data['img'] = $target_file;
}
//print_r($data);
array_push($tempArray, $data);
$jsonData = json_encode($tempArray);
file_put_contents('isimsg.json', $jsonData);
echo "1";
} ?>