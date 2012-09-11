object Timer
{
 def rpm(callback: () => Unit): Unit=
 {
  while (true)
  {
   callback()
   Thread.sleep(1000)
  }
 }
 def hello(): Unit=
 { Console.println("Hello World");}
 def main(args: Array[String]): Unit=
 {
  rpm(hello)
 }
}
