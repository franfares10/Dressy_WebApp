import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import { ThemeProvider } from '@/components/theme-provider';
import { cn } from '@/lib/utils';
import logo from '@/assets/logo.png';
import Image from 'next/image';
import Link from 'next/link';
const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'Create Next App',
  description: 'Generated by create next app',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang='en' suppressHydrationWarning>
      <body
        className={cn(
          'min-h-screen bg-background text-foreground antialiased mx-auto ',
          inter.className
        )}
      >
        <ThemeProvider
          attribute='class'
          defaultTheme='dark'
          enableSystem
          disableTransitionOnChange
        >
          <div className='relative h-full w-full bg-slate-950 bg-repeat'>
            <div className='absolute bottom-0 left-[-20%] right-0 top-[-10%] h-[500px] w-[500px] rounded-full bg-[radial-gradient(circle_farthest-side,rgba(255,0,182,.15),rgba(255,255,255,0))]'></div>
            <div className='absolute bottom-0 right-[-20%] top-[-10%] h-[500px] w-[500px] rounded-full bg-[radial-gradient(circle_farthest-side,rgba(255,0,182,.15),rgba(255,255,255,0))]'></div>
          </div>
          <div className='flex flex-col'>
            <header className='fixed backdrop-blur-md z-50 w-full flex items-center justify-center h-[80px] shadow-black/10 shadow-md'>
              <Link href='/'>
                <Image src={logo} alt='logo' />
              </Link>
            </header>
            <div className='mx-auto mt-20'>{children}</div>
          </div>
        </ThemeProvider>
      </body>
    </html>
  );
}
