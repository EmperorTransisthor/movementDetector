<?php

namespace App;

class Config
{

    public static function getPhotoPath(): string
    {
        return '/resources/photo.jpg';
    }

    public static function getLocationPath(): string
    {
        return '/../lora_app/resource/gps.txt';
    }

}