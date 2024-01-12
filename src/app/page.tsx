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
import { Label } from '@/components/ui/label';
import { Badge } from '@/components/ui/badge';
import { GithubIcon } from 'lucide-react';
import Link from 'next/link';

export default function Home() {
  return (
    <main className='flex flex-col items-center justify-start min-h-screen gap-y-4 overflow-x-hidden w-full max-w-sm mx-auto md:max-w-2xl lg:max-w-4xl xl:max-w-6xl'>
      <section className='text-center flex items-center justify-center flex-col py-20'>
        <Label className='text-6xl text-wrap text-foreground font-semibold py-4 text-left'>
          The Virtual Dressing Room
        </Label>
        <Label className='text-2xl text-wrap text-foreground font-light mt-1 text-left'>
          Dress the newest clothes from the best brands in the market,
        </Label>
        <Label className='text-2xl text-wrap text-foreground font-light text-left'>
          without leaving your home.
        </Label>
        <Link href={'https://github.com/franfares10/Dressy_WebApp'}>
          <Badge className='mt-4 bg-primary rounded-full py-2 px-4 text-center text-wrap text-md'>
            <GithubIcon className='mr-2' /> Code
          </Badge>
        </Link>
      </section>
      <section>
        <h2 className='text-4xl text-wrap text-primary font-extrabold py-4 text-left'>
          Remeras
        </h2>
        <ClothesCarousel />
      </section>
      <section>
        <h2 className='text-4xl text-wrap text-primary font-extrabold py-4 text-left'>
          Pantalones
        </h2>
        <ClothesCarousel />
      </section>
      <section>
        <h2 className='text-4xl text-wrap text-primary font-extrabold py-4 text-left'>
          Zapatillas
        </h2>
        <ClothesCarousel />
      </section>
      <section>
        <h2 className='text-4xl text-wrap text-primary font-extrabold py-4 text-left'>
          Camperas
        </h2>
        <ClothesCarousel />
      </section>
    </main>
  );
}
