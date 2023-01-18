<?php

namespace App\Controller;

use App\Config;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\BinaryFileResponse;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\HttpKernel\Exception\NotFoundHttpException;
use Symfony\Component\Routing\Annotation\Route;

class AppController extends AbstractController
{

    #[Route('', name: 'index', methods: 'GET')]
    public function index(): Response
    {
        $photo = $this->photoInfo($this->getPhotoPath());

        return $this->render('index.html.twig', [
            'latitude' => '52.19712139157508',
            'longitude' => '21.191097581472455',
            'photo' => $photo
        ]);
    }

    private function photoInfo(string $path): bool
    {
        if (file_exists($path) && is_file($path)) {
            if (stat($path)['mtime'] + 30 < time()) {
                return true;
            }
        }
        return false;
    }

    private function getPhotoPath(): string
    {
        return $this->getParameter('kernel.project_dir') . Config::getPhotoPath();
    }

    #[Route('photo', name: 'photo', methods: 'GET')]
    public function photo(): Response
    {
        $path = $this->getPhotoPath();
        if (!$this->photoInfo($path)) {
            throw new NotFoundHttpException();
        }

        return new BinaryFileResponse($path);
    }

    #[Route('photo-upload', name: 'photo_upload', methods: 'POST')]
    public function photoUpload(Request $request): Response
    {
        $file = $request->files->get('file');
        var_dump($file);
        return $this->json([]);
    }

}