import '../assets/css/Footer.css'

const Footer = () => {
  return (
    <footer className="footer">
      <div className="footerTop">

        {/* Marca */}
        <div>
          <div className="footerBrandName">EPS Izel</div>
          <p className="footerBrandDesc">
            Somos un hospital comprometido con la salud de nuestra comunidad.
            Ofrecemos atención médica integral con calidad, empatía y tecnología.
          </p>
          <div className="socialIcons">
            <button className="socialBtn">
              <svg viewBox="0 0 24 24"><path d="M18 2h-3a5 5 0 00-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 011-1h3z"/></svg>
            </button>
            <button className="socialBtn">
              <svg viewBox="0 0 24 24"><rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1.5"/></svg>
            </button>
            <button className="socialBtn">
              <svg viewBox="0 0 24 24"><path d="M22.54 6.42a2.78 2.78 0 00-1.95-1.96C18.88 4 12 4 12 4s-6.88 0-8.59.46A2.78 2.78 0 001.46 6.42 29 29 0 001 12a29 29 0 00.46 5.58 2.78 2.78 0 001.95 1.96C5.12 20 12 20 12 20s6.88 0 8.59-.46a2.78 2.78 0 001.95-1.96A29 29 0 0023 12a29 29 0 00-.46-5.58z"/><polygon points="9.75 15.02 15.5 12 9.75 8.98 9.75 15.02" fill="#171738"/></svg>
            </button>
          </div>
        </div>

        {/* Contacto */}
        <div>
          <div className="footerColTitle">Contacto</div>
          <div className="footerContactItem">
            <span className="footerContactIcon"></span>
            <span className="footerContactText">Carrera 10a#13b-74s, Soacha</span>
          </div>
          <div className="footerContactItem">
            <span className="footerContactIcon"></span>
            <span className="footerContactText">Tel: 3125278094</span>
          </div>
          <div className="footerContactItem">
            <span className="footerContactIcon"></span>
            <span className="footerContactText">epsizel@gmail.com</span>
          </div>
          <div className="footerContactItem">
            <span className="footerContactIcon"></span>
            <span className="footerContactText">Lunes a Sábado: 8:00am – 5:00pm</span>
          </div>
        </div>

        {/* Servicios */}
        <div>
          <div className="footerColTitle">Servicios</div>
          <ul className="footerLinks">
            <li><a href="#">Consulta General</a></li>
            <li><a href="#">Odontologia</a></li>
            <li><a href="#">Pediatria</a></li>
          </ul>
        </div>

      </div>
      <div className="footerBottom">
        <p>© EPS Izel. Todos los derechos reservados.</p>
      </div>
    </footer>
  )
}

export default Footer
