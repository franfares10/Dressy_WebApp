import { Input } from '@/components/ui/input';
import { Slider } from '@/components/ui/slider';
import { ClothesFilter } from '@/components/ux/filters';
import Image from 'next/image';
import { Card, CardContent } from '@/components/ui/card';
import Autoplay from 'embla-carousel-autoplay';
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselNext,
  CarouselPrevious,
} from '@/components/ui/carousel';
import React from 'react';
import { ClothesCarousel } from '@/components/ux/clothes-carousel';

export default function Home() {
  return (
    <main className='flex flex-col items-center justify-start w-full min-h-screen gap-y-4 overflow-x-hidden'>
      <section className='w-full max-w-sm mx-auto md:max-w-2xl lg:max-w-4xl xl:max-w-6xl'>
        <h2 className='text-4xl text-wrap text-primary font-extrabold py-4 text-left'>
          Remeras
        </h2>
        <ClothesCarousel />
      </section>
      <section className='w-full max-w-sm mx-auto md:max-w-2xl lg:max-w-4xl xl:max-w-6xl'>
        <h2 className='text-4xl text-wrap text-primary font-extrabold py-4 text-left'>
          Pantalones
        </h2>
        <ClothesCarousel />
      </section>
      <section className='w-full max-w-sm mx-auto md:max-w-2xl lg:max-w-4xl xl:max-w-6xl'>
        <h2 className='text-4xl text-wrap text-primary font-extrabold py-4 text-left'>
          Zapatillas
        </h2>
        <ClothesCarousel />
      </section>
      <section className='w-full max-w-sm mx-auto md:max-w-2xl lg:max-w-4xl xl:max-w-6xl'>
        <h2 className='text-4xl text-wrap text-primary font-extrabold py-4 text-left'>
          Camperas
        </h2>
        <ClothesCarousel />
      </section>
    </main>
  );
}
