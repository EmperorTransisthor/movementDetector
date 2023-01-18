<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;

class AppController extends AbstractController
{

    #[Route('', name: 'index', methods: 'GET')]
    public function index(): Response
    {
        $photo = false;
        return $this->render('index.html.twig', [
            'latitude' => '52.19712139157508',
            'longitude' => '21.191097581472455',
            'photo' => $photo
        ]);
    }

    #[Route('photo', name: 'photo', methods: 'GET')]
    public function photo(): Response
    {
        $data = [
            'latitude' => '52.19712139157508',
            'longitude' => '21.191097581472455'
        ];
        return $this->json($data);
    }

    #[Route('photo-upload', name: 'photo_upload', methods: 'POST')]
    public function photoUpload(): Response
    {
        $data = [
            'latitude' => '52.19712139157508',
            'longitude' => '21.191097581472455'
        ];
        return $this->json();
    }

}